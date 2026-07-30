def _get_opponent_element_type(game_state) -> str:
    """Get the opponent's active Pokemon's element type."""
    try:
        active = getattr(game_state, 'opponent_active', None)
        if isinstance(active, dict):
            return active.get("element_type", "") or active.get("type", "") or ""
    except Exception:
        pass
    return ""

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

def _apply_weakness_resistance(damage: int, atk_type: str, defender_id, registry) -> int:
    """Apply weakness (2x) and resistance (-30) to raw damage."""
    if not atk_type or defender_id is None or damage <= 0:
        return damage
    try:
        def_id = int(defender_id) if not isinstance(defender_id, int) else defender_id
        weak = registry.card_weakness.get(def_id, "")
        resist = registry.card_resistance.get(def_id, "")
        if atk_type and weak and atk_type == weak:
            damage *= 2
        if atk_type and resist and atk_type == resist:
            damage = max(0, damage - 30)
    except Exception:
        pass
    return damage

