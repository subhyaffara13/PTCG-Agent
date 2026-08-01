
def resolve_action(candidates, game_state, profile, time_rem, mcts_engine, rules):
    try:
        if "my_deck_count" not in game_state:
            return None, ""
        lethal_override = game_state.get("lethal_action_override")
        if lethal_override and lethal_override in candidates:
            return lethal_override, f"LETHAL BYPASS: Selected {lethal_override} for immediate win."
            
        primary = check_mcts_bypass(candidates, game_state, rules)
        if primary:
            return primary, f"ELITE SEQUENCING BYPASS: Selected {primary} for max info gain."
        seq_engine = SequencingEngine()
        groups = seq_engine.group_actions(candidates)
        
        MIN_CANDIDATES = 3
        selected_candidates = candidates
        for phase in SequencingEngine.PHASE_ORDER:
            phase_actions = groups.get(phase, [])
            if phase_actions:
                escape_actions = [a for a in candidates if a.startswith("attack:") or a == "pass"]
                merged = list(dict.fromkeys(phase_actions + escape_actions))
                if len(merged) >= MIN_CANDIDATES:
                    selected_candidates = merged
                    break
        has_cpp = getattr(mcts_engine, "HAS_CPP", False)
        orig_sims = getattr(mcts_engine, "num_simulations", 150)
        actual_sims = orig_sims
        try:
            if has_cpp:
                if time_rem < 30.0:
                    mcts_engine.num_simulations = 500
                elif time_rem < 80.0:
                    mcts_engine.num_simulations = 1000
                else:
                    mcts_engine.num_simulations = 2000
            else:
                import os
                if os.environ.get("IS_WORKER") == "true" or os.environ.get("SKIP_GAME_LOGS") == "1":
                    mcts_engine.num_simulations = min(120, max(40, int(time_rem * 0.4)))
                else:
                    mcts_engine.num_simulations = max(orig_sims, min(300, int(time_rem * 1.5)))
                
            actual_sims = mcts_engine.num_simulations
            primary = mcts_engine.search(game_state, selected_candidates, time_remaining=time_rem)
        finally:
            mcts_engine.num_simulations = orig_sims

        # HARD RULE: Never pass or retreat when an attack is available and feasible
        if primary in ("pass",) or (primary is not None and primary.startswith("retreat:")):
            attack_candidates = [c for c in candidates if c.startswith("attack:")]
            if attack_candidates:
                # Check if active has enough energy to actually attack
                ac = game_state.get("my_active_pokemon", {})
                can_attack = True
                if isinstance(ac, dict):
                    attached_count = len(ac.get("attached", []) or ac.get("energies", []))
                    active_id = ac.get("id")
                    if active_id is not None:
                        try:
                            from cb_agents.turn_planner_heuristics import _registry
                            min_cost = _registry.get_min_energy_cost(active_id)
                            can_attack = attached_count >= min_cost
                        except Exception:
                            can_attack = attached_count >= 1
                    else:
                        can_attack = attached_count >= 1
                my_status = game_state.get("my_active_status", "")
                if my_status in ("paralyzed", "asleep"):
                    can_attack = False
                if can_attack:
                    primary = attack_candidates[0]
                    return primary, f"ATTACK OVERRIDE: Forced {primary} over pass/retreat. Profile: {profile}."

        return primary, f"MCTS selected {primary} ({orig_sims} -> {actual_sims} sims). Profile: {profile}."
    except Exception as e:
        logger.error(f"resolve_action failed: {e}", exc_info=True)
        fallback = candidates[0] if candidates else "pass"
        return fallback, f"resolve_error: {e}"


def resolve_action(candidates, game_state, profile, time_rem, mcts_engine, rules):
    try:
        if "my_deck_count" not in game_state:
            return None, ""
        lethal_override = game_state.get("lethal_action_override")
        if lethal_override and lethal_override in candidates:
            return lethal_override, f"LETHAL BYPASS: Selected {lethal_override} for immediate win."
            
        primary = check_mcts_bypass(candidates, game_state, rules)
        if primary:
            return primary, f"ELITE SEQUENCING BYPASS: Selected {primary} for max info gain."
        seq_engine = SequencingEngine()
        groups = seq_engine.group_actions(candidates)
        
        MIN_CANDIDATES = 3
        selected_candidates = candidates
        for phase in SequencingEngine.PHASE_ORDER:
            phase_actions = groups.get(phase, [])
            if phase_actions:
                escape_actions = [a for a in candidates if a.startswith("attack:") or a == "pass"]
                merged = list(dict.fromkeys(phase_actions + escape_actions))
                if len(merged) >= MIN_CANDIDATES:
                    selected_candidates = merged
                    break
        has_cpp = getattr(mcts_engine, "HAS_CPP", False)
        orig_sims = getattr(mcts_engine, "num_simulations", 150)
        actual_sims = orig_sims
        try:
            if has_cpp:
                if time_rem < 30.0:
                    mcts_engine.num_simulations = 500
                elif time_rem < 80.0:
                    mcts_engine.num_simulations = 1000
                else:
                    mcts_engine.num_simulations = 2000
            else:
                import os
                if os.environ.get("IS_WORKER") == "true" or os.environ.get("SKIP_GAME_LOGS") == "1":
                    mcts_engine.num_simulations = min(120, max(40, int(time_rem * 0.4)))
                else:
                    mcts_engine.num_simulations = max(orig_sims, min(300, int(time_rem * 1.5)))
                
            actual_sims = mcts_engine.num_simulations
            primary = mcts_engine.search(game_state, selected_candidates, time_remaining=time_rem)
        finally:
            mcts_engine.num_simulations = orig_sims

        # HARD RULE: Never pass or retreat when an attack is available and feasible
        if primary in ("pass",) or (primary is not None and primary.startswith("retreat:")):
            attack_candidates = [c for c in candidates if c.startswith("attack:")]
            if attack_candidates:
                # Check if active has enough energy to actually attack
                ac = game_state.get("my_active_pokemon", {})
                can_attack = True
                if isinstance(ac, dict):
                    attached_count = len(ac.get("attached", []) or ac.get("energies", []))
                    active_id = ac.get("id")
                    if active_id is not None:
                        try:
                            from cb_agents.turn_planner_heuristics import _registry
                            min_cost = _registry.get_min_energy_cost(active_id)
                            can_attack = attached_count >= min_cost
                        except Exception:
                            can_attack = attached_count >= 1
                    else:
                        can_attack = attached_count >= 1
                my_status = game_state.get("my_active_status", "")
                if my_status in ("paralyzed", "asleep"):
                    can_attack = False
                if can_attack:
                    primary = attack_candidates[0]
                    return primary, f"ATTACK OVERRIDE: Forced {primary} over pass/retreat. Profile: {profile}."

        return primary, f"MCTS selected {primary} ({orig_sims} -> {actual_sims} sims). Profile: {profile}."
    except Exception as e:
        logger.error(f"resolve_action failed: {e}", exc_info=True)
        fallback = candidates[0] if candidates else "pass"
        return fallback, f"resolve_error: {e}"


def resolve_action(candidates, game_state, profile, time_rem, mcts_engine, rules):
    try:
        if "my_deck_count" not in game_state:
            return None, ""
        if os.environ.get("FAST_SIM_MODE") == "true":
            from cb_agents.turn_planner_heuristics import sort_actions_heuristically
            sorted_cands = sort_actions_heuristically(candidates, profile, game_state)
            return sorted_cands[0] if sorted_cands else "pass", "FAST_SIM_MODE: Heuristic bypass"
            
        lethal_override = game_state.get("lethal_action_override")
        if lethal_override and lethal_override in candidates:
            return lethal_override, f"LETHAL BYPASS: Selected {lethal_override} for immediate win."
            
        primary = check_mcts_bypass(candidates, game_state, rules)
        if primary:
            return primary, f"ELITE SEQUENCING BYPASS: Selected {primary} for max info gain."
        seq_engine = SequencingEngine()
        groups = seq_engine.group_actions(candidates)
        
        # We restore the professional phase order (Search -> Draw -> Board -> Attack)
        # However, to prevent the AI from being forced into a suicidal or deadlock play
        # (e.g. forced to deck-out or trapped with bad optional cards), we always append
        # the "attack" phase options (which includes 'pass' and 'attack') so it can voluntarily
        # skip the current phase and proceed to combat if the current phase actions are bad.
        # If we have a reasonable number of candidates, let MCTS have a full view of the action space.
        # Otherwise, restrict to the current phase + attacks to manage search depth/time.
        selected_candidates = candidates
        if time_rem < 30.0:
            mcts_engine.num_simulations = 500
        elif time_rem < 80.0:
            mcts_engine.num_simulations = 1000
        else:
            mcts_engine.num_simulations = 2000
            
        primary = mcts_engine.search(game_state, selected_candidates, time_remaining=time_rem)
        return primary, f"MCTS selected {primary} ({mcts_engine.num_simulations} sims, phase restricted). Profile: {profile}."
    except Exception as e:
        logger.error(f"resolve_action failed: {e}", exc_info=True)
        return None, f"resolve_error: {e}"

