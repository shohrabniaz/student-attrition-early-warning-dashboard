from __future__ import annotations
import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ControlResult:
    control_id: str
    title: str
    score: int
    max_score: int
    status: str
    evidence: str

def load_controls(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def evaluate(controls: list[dict]) -> list[ControlResult]:
    out = []
    for c in controls:
        score = int(c.get("score", 0))
        mx = int(c.get("max_score", 100))
        status = "pass" if score >= int(c.get("pass_threshold", 70)) else "gap"
        out.append(ControlResult(c["control_id"], c["title"], score, mx, status, c.get("evidence", "")))
    return out

def summarise(results: list[ControlResult]) -> dict:
    total = sum(r.score for r in results)
    mx = sum(r.max_score for r in results) or 1
    gaps = [r.control_id for r in results if r.status == "gap"]
    return {
        "coverage_percent": round(100.0 * total / mx, 1),
        "control_count": len(results),
        "gap_count": len(gaps),
        "gaps": gaps,
        "results": [asdict(r) for r in results],
    }

def run(data_dir: Path, out_dir: Path) -> dict:
    summary = summarise(evaluate(load_controls(data_dir / "controls.csv")))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "assessment_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
