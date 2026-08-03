import csv
from pathlib import Path
from typing import List


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

