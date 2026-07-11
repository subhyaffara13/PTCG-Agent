from cb_agents.heuristic_pipeline import pipeline

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
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"project_opponent_damage failed: {e}")
    return max_dmg

def check_defensive_retreat_helper(game_state, board_summary) -> str:
    opponent_max_damage = project_opponent_damage_helper(game_state)
    my_hp = getattr(game_state, 'my_active_hp', 0)
    if opponent_max_damage > 0 and opponent_max_damage >= my_hp:
        retreat_actions = list(getattr(game_state, 'legal_retreats', []))
        if retreat_actions:
            return retreat_actions[0]
    return None

def update_opponent_model_helper(orchestrator, game_state):
    from router.bus import OpponentModelPacket
    newly_played = game_state.opponent_revealed if game_state.opponent_revealed else []
    orchestrator.bus.dispatch("OpponentModel", OpponentModelPacket(
        turn=orchestrator.current_turn, newly_played_cards=newly_played,
        revealed_active_pokemon=game_state.opponent_active,
        revealed_bench_count=len(game_state.opponent_bench), revealed_hand_size=game_state.opponent_hand_count,
        revealed_prizes_remaining=game_state.opponent_prizes, revealed_discard=game_state.opponent_discard,
        game_phase="early" if orchestrator.current_turn < 5 else "mid"))

    arch = orchestrator.opponent_model.identified_archetype
    if arch != "unknown" and arch in orchestrator.opponent_model.archetypes:
        pool = orchestrator.opponent_model.archetypes[arch].get("card_pool", [])
        sig = orchestrator.opponent_model.archetypes[arch].get("signature_cards", [])
        new_deck_dict = {}
        for cid in sig:
            try: new_deck_dict[int(cid)] = 4
            except (ValueError, TypeError): pass
        for cid in pool:
            try:
                cid_int = int(cid)
                if cid_int not in new_deck_dict: new_deck_dict[cid_int] = 2
            except (ValueError, TypeError): pass
        if new_deck_dict:
            orchestrator.belief_tracker.assumed_deck = new_deck_dict

def check_lethal_helper(game_state):
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
        my_attached=my_attached)
    return lethal_result

def handle_time_manager_helper(orchestrator, time_elapsed, legal_actions_list, game_state):
    from router.bus import TimePacket
    from cb_agents.heuristic_pipeline import pipeline

    def _get_f(obj, k, default=None):
        if isinstance(obj, dict): return obj.get(k, default)
        return getattr(obj, k, default)

    time_result = orchestrator.bus.dispatch('TimeManager', TimePacket(
        time_elapsed=time_elapsed, time_limit=600.0, legal_actions=legal_actions_list).__dict__)

    t_dir = _get_f(time_result, 'directive')
    t_act = _get_f(time_result, 'action_override')

    if t_dir == 'FORCE_PASS':
        if 'pass' in legal_actions_list:
            return 'pass'
        elif legal_actions_list:
            return legal_actions_list[0]
        else:
            return 'pass'
    if t_act is not None: return t_act
    if t_dir == 'FAST_MOVE':
        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        best_action, best_score = 'pass', -float('inf')
        for a in legal_actions_list:
            s = pipeline.score_action(a, gs_dict)
            if s > best_score:
                best_score, best_action = s, a
        return best_action
    return None