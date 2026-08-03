import csv
from pathlib import Path
from typing import List


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

