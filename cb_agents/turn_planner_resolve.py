import logging
import os
from cb_agents.turn_planner_heuristics import check_mcts_bypass
from cb_agents.sequencing_engine import SequencingEngine

logger = logging.getLogger(__name__)

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
        has_cpp = getattr(mcts_engine, "HAS_CPP", False)
        fast_sim = os.environ.get("FAST_SIM_MODE") == "true"
        actual_sims = orig_sims
        try:
            if has_cpp and not fast_sim:
                if time_rem < 30.0:
                    mcts_engine.num_simulations = 500
                elif time_rem < 80.0:
                    mcts_engine.num_simulations = 1000
                else:
                    mcts_engine.num_simulations = 2000
            else:
                mcts_engine.num_simulations = min(orig_sims, 150)
                
            actual_sims = mcts_engine.num_simulations
            primary = mcts_engine.search(game_state, selected_candidates, time_remaining=time_rem)
        finally:
            mcts_engine.num_simulations = orig_sims
        return primary, f"MCTS selected {primary} ({orig_sims} -> {actual_sims} sims). Profile: {profile}."
    except Exception as e:
        logger.error(f"resolve_action failed: {e}", exc_info=True)
        fallback = candidates[0] if candidates else "pass"
        return fallback, f"resolve_error: {e}"
