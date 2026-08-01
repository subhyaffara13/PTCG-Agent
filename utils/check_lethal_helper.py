
def check_lethal_helper(game_state, boss_prob: float = 0.0):
    my_active = game_state.my_active_pokemon or {}
    my_attached = len(my_active.get("attached", []) or my_active.get("energies", [])) if isinstance(my_active, dict) else 0

    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    max_damage = 0
    
    my_active_id = None
    if isinstance(my_active, dict):
        my_active_id = my_active.get("id")
    else:
        my_active_id = my_active
        
    if my_active_id is not None and getattr(game_state, "legal_attacks", []):
        try:
            card = registry.get_full_skill(my_active_id)
            if card:
                max_damage = card.damage_output
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Lethal helper active skill lookup failed: {e}")
    
    active = game_state.opponent_active
    opp_active_id = None
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Lethal helper opponent active ID parse failed: {e}")
        
    lethal_result = pipeline.check_lethal(
        my_damage=max_damage, opp_hp=game_state.opponent_active_hp,
        legal_attacks=game_state.legal_attacks, opp_active_id=opp_active_id,
        my_hp=game_state.my_active_hp, legal_retreats=game_state.legal_retreats,
        my_attached=my_attached, boss_prob=boss_prob)
    return lethal_result


def check_lethal_helper(game_state):
    my_active = game_state.my_active_pokemon or {}
    my_attached = len(my_active.get("attached", [])) if isinstance(my_active, dict) else 0

    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    max_damage = 0
    
    my_active_id = None
    if isinstance(my_active, dict):
        my_active_id = my_active.get("id")
    else:
        my_active_id = my_active
        
    if my_active_id is not None and getattr(game_state, "legal_attacks", []):
        try:
            card = registry.get_full_skill(my_active_id)
            if card:
                max_damage = card.damage_output
        except:
            pass
    
    active = game_state.opponent_active
    opp_active_id = None
    if active:
        try: opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
        except: pass
        
    lethal_result = pipeline.check_lethal(
        my_damage=max_damage, opp_hp=game_state.opponent_active_hp,
        legal_attacks=game_state.legal_attacks, opp_active_id=opp_active_id,
        my_hp=game_state.my_active_hp, legal_retreats=game_state.legal_retreats,
        my_attached=my_attached)
    return lethal_result


def check_lethal_helper(game_state, boss_prob: float = 0.0):
    my_active = game_state.my_active_pokemon or {}
    my_attached = len(my_active.get("attached", []) or my_active.get("energies", [])) if isinstance(my_active, dict) else 0

    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    max_damage = 0
    
    my_active_id = None
    if isinstance(my_active, dict):
        my_active_id = my_active.get("id")
    else:
        my_active_id = my_active
        
    if my_active_id is not None and getattr(game_state, "legal_attacks", []):
        try:
            card = registry.get_full_skill(my_active_id)
            if card:
                max_damage = card.damage_output
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Lethal helper active skill lookup failed: {e}")
    
    active = game_state.opponent_active
    opp_active_id = None
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Lethal helper opponent active ID parse failed: {e}")
        
    lethal_result = pipeline.check_lethal(
        my_damage=max_damage, opp_hp=game_state.opponent_active_hp,
        legal_attacks=game_state.legal_attacks, opp_active_id=opp_active_id,
        my_hp=game_state.my_active_hp, legal_retreats=game_state.legal_retreats,
        my_attached=my_attached, boss_prob=boss_prob)
    return lethal_result

