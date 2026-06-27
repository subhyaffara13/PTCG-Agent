"""Helper functions extracted from analyze_kaggle_losses.py."""


def get_deck_from_state(player_state) -> list:
    obs = player_state.get("observation", {}) or {}
    curr = obs.get("current", {}) or {}
    players = curr.get("players", [])
    if not players:
        return []
    for p in players:
        deck = p.get("deck", [])
        if deck:
            return deck
    return []
