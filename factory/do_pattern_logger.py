import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from factory.do_pattern_analysis import run_winning_analysis

logger = logging.getLogger("DoPatternLogger")

def load_dos(dos_file: Path) -> Dict[str, Any]:
    if dos_file.exists():
        try:
            return json.loads(dos_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "deck_dos": [],
        "behavior_dos": [],
        "deck_stats": {}
    }

def save_dos(dos_file: Path, learned_dos: dict):
    try:
        dos_file.write_text(json.dumps(learned_dos, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save learned do's: {e}")
