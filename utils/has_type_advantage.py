
def has_type_advantage(my_active_id, opp_active_id) -> bool:
    """Check if our active Pokémon has type advantage (2x weakness) over opponent's active."""
    try:
        if my_active_id is None or opp_active_id is None:
            return False
        my_type = _registry.card_poke_type.get(int(my_active_id), "")
        opp_weakness = _registry.card_weakness.get(int(opp_active_id), "")
        if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
            return True
    except Exception:
        pass
    return False


def has_type_advantage(my_active_id, opp_active_id) -> bool:
    """Check if our active Pokémon has type advantage (2x weakness) over opponent's active."""
    try:
        if my_active_id is None or opp_active_id is None:
            return False
        my_type = _registry.card_poke_type.get(int(my_active_id), "")
        opp_weakness = _registry.card_weakness.get(int(opp_active_id), "")
        if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
            return True
    except Exception:
        pass
    return False

