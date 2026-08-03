import json
from datetime import datetime
from pathlib import Path


def write_deck_report(archetype: str, scores: dict, weak_metric: str, dest: Path):
    report = {
        "timestamp": datetime.now().isoformat(), "archetype": archetype,
        "deck_score": scores["deck_score"], "metrics": scores["metrics"],
        "card_count": 60, "candidates_evaluated": 5, "weak_metric_addressed": weak_metric
    }
    dest.write_text(json.dumps(report, indent=2), encoding="utf-8")

