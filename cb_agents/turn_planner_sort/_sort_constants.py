import json
from pathlib import Path
_PRIORITY_RULES = []
try:
    for _pr_path in [Path("skills/priority_rules.json"), Path(__file__).resolve().parent.parent / "skills" / "priority_rules.json"]:
        if _pr_path.exists():
            _pr_data = json.loads(_pr_path.read_text(encoding="utf-8"))
            _PRIORITY_RULES = _pr_data.get("rules", [])
            break
except Exception:
    pass
_EARLY_BENCH_ORDER = ["play_trainer:", "ability:", "bench:", "retreat:", "attack:", "evolve:", "attach_energy:", "pass"]
