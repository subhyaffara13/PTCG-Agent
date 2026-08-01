
def _load_optimized_deck(custom_path: str | None = None) -> list[int]:
    """Load the best deck from the optimizer pipeline output."""
    import csv
    paths = [custom_path] if custom_path else ["submission/deck.csv", "staging/deck_new.csv", "cb_agents/deck_new.csv", "deck.csv"]
    for deck_path in paths:
        p = Path(deck_path)
        if p.exists():
            try:
                deck = []
                with open(p, "r", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        deck.extend([int(row["card_id"])] * int(row["count"]))
                if len(deck) == 60:
                    logger.info("Loaded optimized deck from %s (%d cards)", deck_path, len(deck))
                    return deck
            except Exception as e:
                logger.warning("Failed to load deck from %s: %s", deck_path, e)
    logger.warning("No optimized deck found, using fallback")
    return [957]*3 + [979]*3 + [37]*3 + [210]*3 + [1121]*1 + [1227]*4 + [1152]*4 + [1210]*3 + [1194]*3 + [1198]*1 + [1229]*1 + [1134]*1 + [1097]*4 + [1182]*4 + [1102]*1 + [1086]*4 + [1123]*1 + [1081]*1 + [1122]*1 + [6]*8 + [4]*6

