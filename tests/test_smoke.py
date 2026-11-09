from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.engine import run  # noqa: E402

def test_run_produces_output():
    out = ROOT / "output" / "test_run"
    if out.exists():
        for f in out.glob("*"):
            if f.is_file():
                f.unlink()
    summary = run(ROOT / "data", out)
    assert isinstance(summary, dict)
    assert out.exists()
    assert any(out.glob("*.json"))

if __name__ == "__main__":
    test_run_produces_output()
    print("smoke_ok")
