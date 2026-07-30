import logging
logger = logging.getLogger(__name__)

def configure_simulations(mcts_engine, time_rem: float, candidates: list) -> tuple:
    has_cpp = getattr(mcts_engine, "HAS_CPP", False)
    orig_sims = getattr(mcts_engine, "num_simulations", 150)
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
    except Exception:
        pass
    return mcts_engine.num_simulations, orig_sims

def select_candidate_group(candidates: list, groups: dict) -> list:
    MIN_CANDIDATES = 3
    from cb_agents.sequencing_engine import SequencingEngine
    for phase in SequencingEngine.PHASE_ORDER:
        phase_actions = groups.get(phase, [])
        if phase_actions:
            escape_actions = [a for a in candidates if a.startswith("attack:") or a == "pass"]
            merged = list(dict.fromkeys(phase_actions + escape_actions))
            if len(merged) >= MIN_CANDIDATES:
                return merged
    return candidates
