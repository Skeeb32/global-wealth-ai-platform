"""Strict contracts, an allowlisted metric registry, and decimal calculations."""
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
import hashlib
import json
import re


class ValidationError(ValueError):
    """A submitted contract is invalid."""


def canonical(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: dict) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def money(value: object, field: str) -> Decimal:
    # A bounded string contract avoids binary floats and unbounded arithmetic.
    if not isinstance(value, str) or not re.fullmatch(r"-?\d{1,18}(?:\.\d{1,6})?", value):
        raise ValidationError(f"{field} must be a decimal string (18 integer, 6 fractional digits maximum)")
    return Decimal(value)


def identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,99}", value):
        raise ValidationError(f"{field} must be a 1–100 character identifier")
    return value


def timestamp(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValidationError("extracted_at must be an ISO timestamp with timezone")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError("invalid extracted_at") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValidationError("extracted_at must include timezone")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class Metric:
    metric_id: str = "synthetic_nav"
    version: str = "1.0.0"
    formula: str = "assets_minus_liabilities_v1"
    definition: str = "Synthetic total assets minus total liabilities; not a business-approved fund metric."
    currency: str = "USD"
    quantum: str = "0.01"
    rounding: str = "ROUND_HALF_EVEN"
    tolerance: str = "0.01"
    max_age_hours: int = 24
    effective_from: str = "2026-01-01"
    effective_to: str = "2026-12-31"
    approval_status: str = "demo_only"
    owner: str = "synthetic-demo-owner"


class Registry:
    """Explicit version selection; no arbitrary formulas or dynamic evaluation."""
    def __init__(self):
        self._metrics = {("synthetic_nav", "1.0.0"): Metric()}

    def get(self, metric_id: str, version: str) -> Metric:
        try:
            return self._metrics[(metric_id, version)]
        except KeyError as exc:
            raise ValidationError("unknown metric or version") from exc

    def list(self) -> list[dict]:
        return [asdict(metric) for metric in self._metrics.values()]


@dataclass(frozen=True)
class Snapshot:
    snapshot_id: str
    entity_id: str
    period: str
    currency: str
    extracted_at: str
    assets: str
    liabilities: str
    expected: str
    schema_version: str
    synthetic: bool

    @classmethod
    def parse(cls, data: dict, metric: Metric, now: datetime) -> "Snapshot":
        if not isinstance(data, dict) or set(data) != set(cls.__dataclass_fields__):
            raise ValidationError("snapshot must contain exactly the documented fields")
        if data["synthetic"] is not True or data["schema_version"] != "1.0":
            raise ValidationError("only synthetic schema version 1.0 is supported")
        for field in ("snapshot_id", "entity_id"):
            identifier(data[field], field)
        if data["currency"] != metric.currency:
            raise ValidationError("currency does not match metric")
        try:
            period = date.fromisoformat(data["period"])
        except (TypeError, ValueError) as exc:
            raise ValidationError("period must be YYYY-MM-DD") from exc
        if period.isoformat() != data["period"]:
            raise ValidationError("period must be YYYY-MM-DD")
        if not date.fromisoformat(metric.effective_from) <= period <= date.fromisoformat(metric.effective_to):
            raise ValidationError("metric is not effective for this period")
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValidationError("evaluation time must include timezone")
        extracted = timestamp(data["extracted_at"])
        age = now.astimezone(timezone.utc) - extracted
        if age < timedelta(0) or age > timedelta(hours=metric.max_age_hours):
            raise ValidationError("snapshot is future-dated or stale")
        if period > extracted.date():
            raise ValidationError("period cannot be after extraction date")
        for field in ("assets", "liabilities", "expected"):
            amount = money(data[field], field)
            if field != "expected" and amount < 0:
                raise ValidationError(f"{field} must be non-negative")
        return cls(**data)


def calculate(snapshot: Snapshot, metric: Metric) -> dict:
    if metric.formula != "assets_minus_liabilities_v1":
        raise ValidationError("unsupported formula")
    if metric.quantum != "0.01" or metric.rounding != "ROUND_HALF_EVEN":
        raise ValidationError("unsupported precision policy")
    with localcontext() as context:
        context.prec = 40
        actual = (money(snapshot.assets, "assets") - money(snapshot.liabilities, "liabilities")).quantize(
            Decimal(metric.quantum), rounding=ROUND_HALF_EVEN
        )
        expected = money(snapshot.expected, "expected")
        if expected != expected.quantize(Decimal(metric.quantum), rounding=ROUND_HALF_EVEN):
            raise ValidationError("reference result must already be rounded to cents")
        delta = actual - expected
        tolerance = money(metric.tolerance, "tolerance")
        if tolerance < 0:
            raise ValidationError("tolerance must be non-negative")
        return {"actual": str(actual), "expected": format(expected, ".2f"),
                "delta": format(delta, ".2f"), "tolerance": metric.tolerance,
                "reconciliation": "matched" if abs(delta) <= tolerance else "exception"}
