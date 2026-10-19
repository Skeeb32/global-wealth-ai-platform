"""Run with PYTHONPATH=src python3 -m wealth_platform --help."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import sys

from .core import Registry, ValidationError, timestamp
from .workflow import Workflow


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Synthetic metric and reconciliation demo; local use only")
    parser.add_argument("--db", default="demo.sqlite3")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("metrics")
    commands.add_parser("runs")
    show = commands.add_parser("show")
    show.add_argument("run_id")
    submit = commands.add_parser("run")
    submit.add_argument("input", type=Path)
    submit.add_argument("--run-id", required=True)
    submit.add_argument("--actor", required=True)
    submit.add_argument("--metric", default="synthetic_nav")
    submit.add_argument("--version", default="1.0.0")
    submit.add_argument("--as-of", help="Demo evaluation clock, ISO timestamp with timezone")
    review = commands.add_parser("review")
    review.add_argument("run_id")
    review.add_argument("--reviewer", required=True)
    review.add_argument("--decision", choices=["approved", "rejected"], required=True)
    review.add_argument("--evidence", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "metrics":
            result = Registry().list()
        else:
            with Workflow(args.db) as workflow:
                if args.command == "run":
                    if args.input.stat().st_size > 1_000_000:
                        raise ValidationError("input exceeds 1 MB limit")
                    data = json.loads(args.input.read_text(), object_pairs_hook=reject_duplicates)
                    now = timestamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
                    result = workflow.submit(data, run_id=args.run_id, actor=args.actor,
                                             metric_id=args.metric, version=args.version, now=now)
                elif args.command == "review":
                    result = workflow.review(args.run_id, reviewer=args.reviewer,
                                             decision=args.decision, evidence=args.evidence)
                elif args.command == "show":
                    result = workflow.get(args.run_id)
                else:
                    result = workflow.list()
        print(json.dumps(result, indent=2))
        return 0
    except (ValidationError, OSError, UnicodeError, json.JSONDecodeError, sqlite3.Error) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
