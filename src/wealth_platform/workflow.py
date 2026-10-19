"""Transactional local workflow store. Not an authenticated production service."""
from dataclasses import asdict
from datetime import datetime, timezone
import json
import sqlite3

from .core import Registry, Snapshot, ValidationError, calculate, canonical, digest, identifier


class Workflow:
    def __init__(self, database: str):
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                fingerprint TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reviews (
                run_id TEXT PRIMARY KEY REFERENCES runs(run_id),
                reviewer TEXT NOT NULL,
                decision TEXT NOT NULL CHECK(decision IN ('approved', 'rejected')),
                evidence TEXT NOT NULL,
                reviewed_at TEXT NOT NULL
            );
        """)
        self.registry = Registry()

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def submit(self, data: dict, *, run_id: str, actor: str,
               metric_id: str = "synthetic_nav", version: str = "1.0.0",
               now: datetime | None = None) -> dict:
        identifier(run_id, "run_id")
        identifier(actor, "actor")
        metric = self.registry.get(metric_id, version)
        if not isinstance(data, dict):
            raise ValidationError("snapshot must be an object")
        try:
            fingerprint = digest({"source": data, "metric": asdict(metric), "actor": actor})
        except (TypeError, ValueError) as exc:
            raise ValidationError("snapshot must contain finite JSON values") from exc
        # Serialize readers and writers for atomic idempotency and review transitions.
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            old = self.db.execute("SELECT fingerprint FROM runs WHERE run_id=?", (run_id,)).fetchone()
            if old:
                if old["fingerprint"] != fingerprint:
                    raise ValidationError("run_id already exists with different inputs, metric, or actor")
                return self.get(run_id)
            now = now or datetime.now(timezone.utc)
            snapshot = Snapshot.parse(data, metric, now)
            result = calculate(snapshot, metric)
            payload = {"run_id": run_id, "submitted_by": actor,
                       "created_at": now.astimezone(timezone.utc).isoformat(),
                       "state": "pending_review", "result": result,
                       "source": asdict(snapshot), "metric": asdict(metric),
                       "lineage": {"source_sha256": digest(data), "contract_version": snapshot.schema_version,
                                   "calculation_version": metric.version, "engine_version": "0.1.0",
                                   "metric_sha256": digest(asdict(metric))}}
            self.db.execute("INSERT INTO runs VALUES (?, ?, ?)", (run_id, fingerprint, canonical(payload)))
        return self.get(run_id)

    def get(self, run_id: str) -> dict:
        row = self.db.execute("SELECT payload FROM runs WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise ValidationError("run not found")
        result = json.loads(row["payload"])
        review = self.db.execute("SELECT reviewer, decision, evidence, reviewed_at FROM reviews WHERE run_id=?", (run_id,)).fetchone()
        if review:
            result["review"] = dict(review)
            result["state"] = review["decision"]
        return result

    def list(self) -> list[dict]:
        return [self.get(row["run_id"]) for row in self.db.execute("SELECT run_id FROM runs ORDER BY rowid")]

    def review(self, run_id: str, *, reviewer: str, decision: str, evidence: str) -> dict:
        identifier(reviewer, "reviewer")
        if decision not in {"approved", "rejected"}:
            raise ValidationError("decision must be approved or rejected")
        if not isinstance(evidence, str) or not 10 <= len(evidence.strip()) <= 2000:
            raise ValidationError("evidence must contain 10–2000 characters")
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            run = self.get(run_id)
            if run["state"] != "pending_review":
                raise ValidationError("run already reviewed; submit a new run for corrections")
            if reviewer == run["submitted_by"]:
                raise ValidationError("reviewer must differ from submitter")
            self.db.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?)",
                            (run_id, reviewer, decision, evidence.strip(), datetime.now(timezone.utc).isoformat()))
        return self.get(run_id)
