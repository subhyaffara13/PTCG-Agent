
def _get_poke_type_resistance(tc, opp_type: str) -> float:
    """Score type matchup using registry weakness/resistance: +2 resist, -2 weak, 0 neutral."""
    if not opp_type or not tc:
        return 0.0
    try:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
        card_id = tc.id if hasattr(tc, 'id') else None
        if card_id is None:
            return 0.0
        poke_type = registry.card_poke_type.get(int(card_id), "")
        if not poke_type:
            return 0.0
        # Check if our type resists opponent type (opponent's attack is not very effective)
        weak_against_opp = registry.card_weakness.get(int(card_id), "")
        resist_against_opp = registry.card_resistance.get(int(card_id), "")
        opp_type_lower = opp_type.lower()
        if resist_against_opp and resist_against_opp.lower() == opp_type_lower:
            return 2.0  # We resist
        if weak_against_opp and weak_against_opp.lower() == opp_type_lower:
            return -2.0  # We are weak
    except Exception:
        pass
    return 0.0


def _get_poke_type_resistance(tc, opp_type: str) -> float:
    """Score type matchup using registry weakness/resistance: +2 resist, -2 weak, 0 neutral."""
    if not opp_type or not tc:
        return 0.0
    try:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
        card_id = tc.id if hasattr(tc, 'id') else None
        if card_id is None:
            return 0.0
        poke_type = registry.card_poke_type.get(int(card_id), "")
        if not poke_type:
            return 0.0
        # Check if our type resists opponent type (opponent's attack is not very effective)
        weak_against_opp = registry.card_weakness.get(int(card_id), "")
        resist_against_opp = registry.card_resistance.get(int(card_id), "")
        opp_type_lower = opp_type.lower()
        if resist_against_opp and resist_against_opp.lower() == opp_type_lower:
            return 2.0  # We resist
        if weak_against_opp and weak_against_opp.lower() == opp_type_lower:
            return -2.0  # We are weak
    except Exception:
        pass
    return 0.0

