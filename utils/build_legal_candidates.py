
def build_legal_candidates(game_state: dict) -> List[str]:
    """Build a list of legal action strings from game_state fields."""
    if game_state.get("select_prize"):
        prize_opts = game_state.get("legal_prize_options", [])
        candidates = [f"take_prize:{v}" for v in prize_opts]
        if not candidates:
            candidates.append("pass")
        return candidates

    candidates = []

    for k, prefix in [
        ("legal_attacks", "attack"),
        ("legal_evolutions", "evolve"),
        ("legal_attachments", "attach_energy"),
        ("legal_trainers", "play_trainer"),
        ("legal_bench", "bench"),
        ("legal_retreats", "retreat"),
        ("legal_abilities", "ability"),
    ]:
        for val in game_state.get(k, []):
            candidates.append(f"{prefix}:{val}")

    candidates.append("pass")
    return candidates


def build_legal_candidates(game_state: dict) -> List[str]:
    """Build a list of legal action strings from game_state fields."""
    if game_state.get("select_prize"):
        prize_opts = game_state.get("legal_prize_options", [])
        candidates = [f"take_prize:{v}" for v in prize_opts]
        if not candidates:
            candidates.append("pass")
        return candidates

    candidates = []

    for k, prefix in [
        ("legal_attacks", "attack"),
        ("legal_evolutions", "evolve"),
        ("legal_attachments", "attach_energy"),
        ("legal_trainers", "play_trainer"),
        ("legal_bench", "bench"),
        ("legal_retreats", "retreat"),
        ("legal_abilities", "ability"),
    ]:
        for val in game_state.get(k, []):
            candidates.append(f"{prefix}:{val}")

    candidates.append("pass")
    return candidates


def build_legal_candidates(game_state: dict) -> List[str]:
    """Build a list of legal action strings from game_state fields."""
    if game_state.get("select_prize"):
        prize_opts = game_state.get("legal_prize_options", [])
        candidates = [f"take_prize:{v}" for v in prize_opts]
        if not candidates:
            candidates.append("pass")
        return candidates

    candidates = []

    for k, prefix in [
        ("legal_attacks", "attack"),
        ("legal_evolutions", "evolve"),
        ("legal_attachments", "attach_energy"),
        ("legal_trainers", "play_trainer"),
        ("legal_bench", "bench"),
        ("legal_retreats", "retreat"),
        ("legal_abilities", "ability"),
    ]:
        for val in game_state.get(k, []):
            candidates.append(f"{prefix}:{val}")

    candidates.append("pass")
    return candidates

