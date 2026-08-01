
def _load_concede_thresholds() -> tuple:
    try:
        for p in ["logs", "data", "."]:
            rp = Path(p) / "iteration_result.json"
            if rp.exists():
                data = json.loads(rp.read_text(encoding="utf-8"))
                games = data.get("games", {})
                deck_games = [g for k, g in games.items() if k.startswith("deck_test")]
                if len(deck_games) >= 10:
                    wins = sum(1 for g in deck_games if g.get("winner") == "player_b")
                    wr = wins / len(deck_games)
                    if wr < 0.3:
                        return (2, 3, 3)
                    elif wr > 0.7:
                        return (4, 2, 3)
                break
    except Exception:
        pass
    return (2, 3, 2)


def _load_concede_thresholds() -> tuple:
    try:
        for p in ["logs", "data", "."]:
            rp = Path(p) / "iteration_result.json"
            if rp.exists():
                data = json.loads(rp.read_text(encoding="utf-8"))
                games = data.get("games", {})
                deck_games = [g for k, g in games.items() if k.startswith("deck_test")]
                if len(deck_games) >= 10:
                    wins = sum(1 for g in deck_games if g.get("winner") == "player_b")
                    wr = wins / len(deck_games)
                    if wr < 0.3:
                        return (2, 3, 3)
                    elif wr > 0.7:
                        return (4, 2, 3)
                break
    except Exception:
        pass
    return (2, 3, 2)

