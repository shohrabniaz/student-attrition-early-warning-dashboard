from __future__ import annotations
import argparse
import json
from pathlib import Path
from .engine import run

ROOT = Path(__file__).resolve().parents[1]

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Project automation CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run", help="Execute automation against sample/lab data")
    run_p.add_argument("--data", type=Path, default=ROOT / "data")
    run_p.add_argument("--out", type=Path, default=ROOT / "output")
    sub.add_parser("version", help="Show package version")
    args = p.parse_args(argv)
    if args.cmd == "version":
        from . import __version__, PROJECT_SLUG
        print(PROJECT_SLUG, __version__)
        return 0
    summary = run(args.data, args.out)
    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
