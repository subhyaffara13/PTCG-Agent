import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def log_error_to_decisions(decisions_file: Path, reason: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## BUILDER AGENT ERROR — {timestamp}\n**Error:** {reason}\n---\n"
    try:
        with open(decisions_file, "a", encoding="utf-8") as f: f.write(entry)
    except Exception as e:
        logger.error(f"Failed to append error to decisions.md: {e}")
