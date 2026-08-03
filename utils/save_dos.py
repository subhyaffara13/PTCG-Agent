import json
from pathlib import Path


def save_dos(dos_file: Path, learned_dos: dict):
    try:
        dos_file.write_text(json.dumps(learned_dos, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save learned do's: {e}")

