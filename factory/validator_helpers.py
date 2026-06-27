import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_baseline_score(history_file: Path) -> float:
    if history_file.exists():
        try:
            history = json.loads(history_file.read_text(encoding="utf-8").strip())
            if history:
                scores = [item.get("version_score", 0.0) for item in history if item.get("promoted") is True]
                if scores: return max(scores)
        except Exception as e:
            logger.error(f"Failed to load baseline score: {e}")
    return 0.0

def handle_validation_failure(report: dict, check_num: int, reason: str, log_file: Path) -> dict:
    report.update({"all_passed": False, "promoted": False, "failed_check": f"check_{check_num}", "reason": reason})
    check_mapping = {
        1: "syntax", 2: "base_inheritance", 3: "receive_method", 4: "router_boundaries",
        5: "no_auto_submit", 6: "no_api_keys", 7: "time_compliance", 8: "score_improvement",
        9: "staging_integrity"
    }
    name = check_mapping.get(check_num)
    if name: report["checks"][name] = "fail"
    write_validation_log(report, log_file)
    return report

def append_to_history(history_file: Path, record: dict):
    history = []
    if history_file.exists():
        try: history = json.loads(history_file.read_text(encoding="utf-8").strip())
        except: pass
    history.append(record)
    try: history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
    except: pass

def write_validation_log(report: dict, log_file: Path):
    try: log_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    except: pass
