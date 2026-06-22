import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class EvalReporter:
    def __init__(self, log_dir: Path, skills_dir: Path):
        self.log_dir = log_dir
        self.skills_dir = skills_dir

    def load_rubric(self) -> dict:
        try:
            return json.loads((self.skills_dir / "eval_rubric.json").read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to load evaluation rubric: {e}")
            return {"contexts": {}}

    def load_theoretical_min(self) -> int:
        try:
            return json.loads((self.skills_dir / "deck_rubric.json").read_text(encoding="utf-8")).get("theoretical_min_turns", 4)
        except Exception:
            return 4

    def load_eval_state(self, state_file: Path) -> dict:
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text(encoding="utf-8"))
                return {
                    "consecutive_deck_failures": data.get("consecutive_deck_failures", 0),
                    "consecutive_logic_failures": data.get("consecutive_logic_failures", 0)
                }
            except Exception:
                pass
        return {"consecutive_deck_failures": 0, "consecutive_logic_failures": 0}

    def load_log_file(self, filename: str) -> list:
        if not filename: return []
        path = self.log_dir / filename
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8").strip()
                if content:
                    if content.startswith("[") and content.endswith("]"):
                        try:
                            return json.loads(content)
                        except Exception:
                            pass
                    return [json.loads(line) for line in content.splitlines() if line.strip()]
            except Exception as e:
                logger.error(f"Failed to load log file {filename}: {e}")
        return []

    def write_report(self, report: dict):
        try:
            (self.log_dir / "eval_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to write eval_report.json: {e}")
