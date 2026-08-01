
def project_opponent_damage_helper(game_state) -> dict:
    """Returns dict with 'max_damage', 'can_2hko' (bool), and 'opponent_type' (str)."""
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    result = {"max_damage": 0, "can_2hko": False, "opponent_type": ""}
    active = getattr(game_state, 'opponent_active', None)
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
            card = registry.get_full_skill(opp_active_id)
            if card:
                raw_dmg = card.damage_output
                opp_attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
                if opp_attached < max(1, card.energy_cost):
                    raw_dmg = 0
                # Apply weakness/resistance: opponent's attack type vs our active's type
                if raw_dmg > 0:
                    opp_type = registry.card_poke_type.get(opp_active_id, "")
                    my_active = getattr(game_state, 'my_active_pokemon', None) or {}
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else None
                    if my_active_id is not None:
                        raw_dmg = _apply_weakness_resistance(raw_dmg, opp_type, my_active_id, registry)
                result["max_damage"] = raw_dmg
                result["opponent_type"] = _get_opponent_element_type(game_state)
                if isinstance(active, dict) and active.get("id") and raw_dmg > 0:
                    my_hp = getattr(game_state, 'my_active_hp', 100)
                    if raw_dmg < my_hp <= raw_dmg * 2:
                        result["can_2hko"] = True
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"project_opponent_damage failed: {e}")
    return result


def project_opponent_damage_helper(game_state) -> int:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    max_dmg = 0
    active = getattr(game_state, 'opponent_active', None)
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
            card = registry.get_full_skill(opp_active_id)
            if card:
                max_dmg = card.damage_output
        except:
            pass
    return max_dmg


def project_opponent_damage_helper(game_state) -> dict:
    """Returns dict with 'max_damage', 'can_2hko' (bool), and 'opponent_type' (str)."""
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    result = {"max_damage": 0, "can_2hko": False, "opponent_type": ""}
    active = getattr(game_state, 'opponent_active', None)
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
            card = registry.get_full_skill(opp_active_id)
            if card:
                raw_dmg = card.damage_output
                opp_attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
                if opp_attached < max(1, card.energy_cost):
                    raw_dmg = 0
                # Apply weakness/resistance: opponent's attack type vs our active's type
                if raw_dmg > 0:
                    opp_type = registry.card_poke_type.get(opp_active_id, "")
                    my_active = getattr(game_state, 'my_active_pokemon', None) or {}
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else None
                    if my_active_id is not None:
                        raw_dmg = _apply_weakness_resistance(raw_dmg, opp_type, my_active_id, registry)
                result["max_damage"] = raw_dmg
                result["opponent_type"] = _get_opponent_element_type(game_state)
                if isinstance(active, dict) and active.get("id") and raw_dmg > 0:
                    my_hp = getattr(game_state, 'my_active_hp', 100)
                    if raw_dmg < my_hp <= raw_dmg * 2:
                        result["can_2hko"] = True
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"project_opponent_damage failed: {e}")
    return result

