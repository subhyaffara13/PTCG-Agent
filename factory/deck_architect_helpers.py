import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

def write_deck_csv(deck: List[dict], dest: Path):
    counts = {}
    for c in deck:
        cid = str(c["card_id"])
        if cid not in counts:
            counts[cid] = {"card_id": cid, "card_name": c.get("card_name", "Unknown"), "card_type": c.get("card_type", "Trainer"), "count": 0, "ev_score": c.get("ev_score", 0.0)}
        counts[cid]["count"] += 1

    with open(dest, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["card_id", "card_name", "card_type", "count", "ev_score"])
        for row in counts.values():
            writer.writerow([row["card_id"], row["card_name"], row["card_type"], row["count"], row["ev_score"]])

def read_deck_csv(src: Path) -> List[dict]:
    deck = []
    if not src.exists():
        return deck
    with open(src, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            count = int(row.get("count", 1))
            card = {
                "card_id": row.get("card_id"),
                "card_name": row.get("card_name"),
                "card_type": row.get("card_type"),
                "ev_score": float(row.get("ev_score", 0.0))
            }
            deck.extend([dict(card) for _ in range(count)])
    return deck

def write_deck_report(archetype: str, scores: dict, weak_metric: str, dest: Path):
    report = {
        "timestamp": datetime.now().isoformat(), "archetype": archetype,
        "deck_score": scores["deck_score"], "metrics": scores["metrics"],
        "card_count": 60, "candidates_evaluated": 5, "weak_metric_addressed": weak_metric
    }
    dest.write_text(json.dumps(report, indent=2), encoding="utf-8")

def log_error_to_decisions(reason: str, decisions_file: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## DECK ARCHITECT ERROR — {timestamp}\n**Error:** {reason}\n---\n"
    try:
        with open(decisions_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logger.error(f"Failed to log architect error: {e}")
