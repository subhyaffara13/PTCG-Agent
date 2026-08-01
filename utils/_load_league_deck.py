
def _load_league_deck(league_file):
    if not league_file.exists():
        return None
    try:
        import csv
        deck = []
        with open(league_file, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                deck.extend([int(row["card_id"])] * int(row["count"]))
        return deck if len(deck) == 60 else None
    except Exception as e:
        logger.warning(f"Failed to load {league_file.name}: {e}")
        return None

