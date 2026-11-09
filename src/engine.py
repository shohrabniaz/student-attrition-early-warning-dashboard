from __future__ import annotations
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def score_text(text: str, positive: set[str], negative: set[str]) -> float:
    tokens = [t.strip(".,!?").lower() for t in (text or "").split()]
    if not tokens:
        return 0.0
    pos = sum(1 for t in tokens if t in positive)
    neg = sum(1 for t in tokens if t in negative)
    return round((pos - neg) / len(tokens), 4)

def analyse(rows: list[dict]) -> dict:
    positive = {"good", "great", "ok", "resolved", "safe", "legit", "ham"}
    negative = {"bad", "phish", "malware", "urgent", "fraud", "spam", "breach", "fail", "risk"}
    labeled = []
    for r in rows:
        text = r.get("text") or r.get("subject") or r.get("message") or ""
        s = score_text(text, positive, negative)
        label = r.get("label") or ("risk" if s < 0 else "benign")
        labeled.append({**r, "score": s, "predicted": "risk" if s < 0 else "benign", "label": label})
    by = Counter(x["predicted"] for x in labeled)
    matched = sum(1 for x in labeled if x.get("label") and x["label"] == x["predicted"])
    return {
        "row_count": len(labeled),
        "prediction_counts": dict(by),
        "accuracy_if_labeled": round(matched / max(len(labeled), 1), 3),
        "samples": labeled[:10],
    }

def metric_dashboard(rows: list[dict], metric_col: str = "value") -> dict:
    series = defaultdict(list)
    for r in rows:
        key = r.get("category") or r.get("day") or "all"
        try:
            series[key].append(float(r.get(metric_col) or r.get("metric") or 0))
        except ValueError:
            continue
    summary = {
        k: {"count": len(v), "avg": round(sum(v)/len(v), 2) if v else 0, "max": max(v) if v else 0, "min": min(v) if v else 0}
        for k, v in series.items()
    }
    return {"categories": summary, "category_count": len(summary)}

def run(data_dir: Path, out_dir: Path) -> dict:
    rows = load_rows(data_dir / "dataset.csv")
    if rows and ("text" in rows[0] or "subject" in rows[0] or "message" in rows[0]):
        summary, name = analyse(rows), "ai_analysis.json"
    else:
        summary, name = metric_dashboard(rows), "analytics_summary.json"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
