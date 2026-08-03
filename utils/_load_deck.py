import os

def _load_deck(path: str) -> list:
    import csv
    from factory.game_runner import DEFAULT_DECK
    if not os.path.exists(path):
        return DEFAULT_DECK
    try:
        deck = []
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                deck.extend([int(row["card_id"])] * int(row["count"]))
        if len(deck) == 60:
            return deck
    except Exception:
        pass
    return DEFAULT_DECK


def _load_deck(path: str) -> list:
    import csv
    from factory.game_runner import DEFAULT_DECK
    if not os.path.exists(path):
        return DEFAULT_DECK
    try:
        deck = []
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                deck.extend([int(row["card_id"])] * int(row["count"]))
        if len(deck) == 60:
            return deck
    except Exception:
        pass
    return DEFAULT_DECK

