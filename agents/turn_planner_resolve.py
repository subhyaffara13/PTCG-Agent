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
            return None, "FAST_SIM_MODE: Heuristic bypass"
            
        lethal_override = game_state.get("lethal_action_override")
        if lethal_override and lethal_override in candidates:
            return lethal_override, f"LETHAL BYPASS: Selected {lethal_override} for immediate win."
            
        primary = check_mcts_bypass(candidates, game_state, rules)
        if primary:
            return primary, f"ELITE SEQUENCING BYPASS: Selected {primary} for max info gain."
        seq_engine = SequencingEngine()
        groups = seq_engine.group_actions(candidates)
        
        selected_candidates = candidates
        for phase in SequencingEngine.PHASE_ORDER:
            if groups.get(phase):
                selected_candidates = groups[phase]
                break
                
        if time_rem < 30.0:
            mcts_engine.num_simulations = 10
        elif time_rem < 80.0:
            mcts_engine.num_simulations = 25
        else:
            mcts_engine.num_simulations = 50
            
        primary = mcts_engine.search(game_state, selected_candidates, time_remaining=time_rem)
        return primary, f"MCTS selected {primary} ({mcts_engine.num_simulations} sims, phase restricted). Profile: {profile}."
    except Exception as e:
        logger.error(f"resolve_action failed: {e}", exc_info=True)
        return None, f"resolve_error: {e}"
