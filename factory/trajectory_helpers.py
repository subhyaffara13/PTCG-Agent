import json
import gzip
import time
from pathlib import Path
from typing import Dict, Any

def get_new_file_path(log_dir: Path) -> Path:
    timestamp = int(time.time())
    return log_dir / f"trajectory_{timestamp}.jsonl.gz"

def prepare_match_record(record: Dict[str, Any]) -> Dict[str, Any]:
    if "elite_metrics" not in record:
        record["elite_metrics"] = {
            "sequencing_efficiency": 1.0,
            "discard_awareness_triggers": 0,
            "sniper_disruptions": 0
        }
    return record
