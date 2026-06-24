import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def append_and_flush_logs(log_file: Path, buffer: list):
    """Write buffered logs to disk and clear buffer."""
    if not buffer:
        return
    try:
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    pass
        logs.extend(buffer)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to flush logs to {log_file}: {e}")
    buffer.clear()
