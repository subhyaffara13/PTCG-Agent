import pathlib

def _run_gauntlet_guard():
    from factory.gauntlet_runner import GauntletRunner
    paths = ["submission/deck.csv", "staging/deck_new.csv", "cb_agents/deck_new.csv", "deck.csv"]
    cand_deck = []
    for p_str in paths:
        p = pathlib.Path(p_str)
        if p.exists():
            import csv
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        cand_deck.extend([int(row["card_id"])] * int(row["count"]))
                if len(cand_deck) == 60:
                    break
            except Exception:
                pass
    if len(cand_deck) != 60:
        from factory.game_runner import DEFAULT_DECK
        cand_deck = list(DEFAULT_DECK)
    res = GauntletRunner().run_gauntlet(cand_deck, num_games_per_stage=1)
    return res.get("win_rate", 0.0) if isinstance(res, dict) else float(res)

