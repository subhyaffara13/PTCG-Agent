
def fast_clone_state(gs: dict) -> dict:
    clone = dict(gs)
    if "my_hand" in clone and isinstance(clone["my_hand"], list):
        clone["my_hand"] = list(clone["my_hand"])
    if "my_bench" in clone and isinstance(clone["my_bench"], list):
        clone["my_bench"] = [dict(p) if isinstance(p, dict) else p for p in clone["my_bench"]]
    if "legal_actions" in clone and isinstance(clone["legal_actions"], list):
        clone["legal_actions"] = list(clone["legal_actions"])
    # Deep-clone active pokemon dicts to prevent MCTS rollout mutations
    if "my_active_pokemon" in clone and isinstance(clone["my_active_pokemon"], dict):
        clone["my_active_pokemon"] = dict(clone["my_active_pokemon"])
        if "attached" in clone["my_active_pokemon"]:
            clone["my_active_pokemon"]["attached"] = list(clone["my_active_pokemon"]["attached"])
    if "opponent_active" in clone and isinstance(clone["opponent_active"], dict):
        clone["opponent_active"] = dict(clone["opponent_active"])
    if "opponent_active_pokemon" in clone and isinstance(clone["opponent_active_pokemon"], dict):
        clone["opponent_active_pokemon"] = dict(clone["opponent_active_pokemon"])
    return clone


def fast_clone_state(gs: dict) -> dict:
    clone = dict(gs)
    for k in ["my_hand", "my_discard", "opponent_discard", "my_deck", "opponent_deck", "my_prizes", "legal_actions"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = list(clone[k])

    if "my_decklist" in clone and isinstance(clone["my_decklist"], dict):
        clone["my_decklist"] = dict(clone["my_decklist"])

    for k in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if k in clone and isinstance(clone[k], dict):
            clone[k] = _fast_poke_clone(clone[k])

    for k in ["my_bench", "opponent_bench"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = [_fast_poke_clone(p) if isinstance(p, dict) else p for p in clone[k]]
    return clone


def fast_clone_state(gs: dict) -> dict:
    clone = dict(gs)
    for k in ["my_hand", "my_discard", "opponent_discard", "my_deck", "opponent_deck", "my_prizes", "legal_actions"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = list(clone[k])

    if "my_decklist" in clone and isinstance(clone["my_decklist"], dict):
        clone["my_decklist"] = dict(clone["my_decklist"])

    for k in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if k in clone and isinstance(clone[k], dict):
            clone[k] = _fast_poke_clone(clone[k])

    for k in ["my_bench", "opponent_bench"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = [_fast_poke_clone(p) if isinstance(p, dict) else p for p in clone[k]]
    return clone

