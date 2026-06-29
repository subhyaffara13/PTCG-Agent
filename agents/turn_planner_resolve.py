import logging
import os
from agents.turn_planner_heuristics import check_mcts_bypass
from agents.sequencing_engine import SequencingEngine

logger = logging.getLogger(__name__)

def resolve_action(candidates, game_state, profile, time_rem, mcts_engine, rules):
    try:
        if "my_deck_count" not in game_state:
            return None, ""
        if os.environ.get("FAST_SIM_MODE") == "true":
            from agents.turn_planner_heuristics import sort_actions_heuristically
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
        selected_candidates = []
        for phase in SequencingEngine.PHASE_ORDER:
            if groups.get(phase):
                selected_candidates = groups[phase].copy()
                if phase != "attack" and groups.get("attack"):
                    selected_candidates.extend(groups["attack"])
                break
                
        if not selected_candidates:
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
