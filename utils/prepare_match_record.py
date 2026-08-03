from typing import Any, Dict

def prepare_match_record(record: Dict[str, Any]) -> Dict[str, Any]:
    if "elite_metrics" not in record:
        record["elite_metrics"] = {
            "sequencing_efficiency": 1.0,
            "discard_awareness_triggers": 0,
            "sniper_disruptions": 0
        }
    return record

