import sys
import time
import logging
from pathlib import Path
from factory.game_logger import GameLogger
from factory.game_agent_wrapper import CABTAgentWrapper

logger = logging.getLogger(__name__)

def _parallel_game_worker(log_dir: str, label: str, v_a: str, v_b: str, 
                          deck_a: list[int], deck_b: list[int], use_staging_a: bool, use_staging_b: bool) -> dict:
    import os
    os.environ["FAST_SIM_MODE"] = "true"
    saved_path = list(sys.path)
    try:
        cwd_resolved = Path.cwd().resolve()
        sys.path = [p for p in sys.path if p and Path(p).resolve() != cwd_resolved]
        import logging
        import os
        import contextlib
        logging.getLogger("kaggle_environments").setLevel(logging.WARNING)
        with open(os.devnull, 'w') as fnull:
            with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                from kaggle_environments import make
    finally:
        sys.path = saved_path

    start_time = time.time()
    g_logger = GameLogger(log_dir=log_dir)
    g_logger.timestamp_str = f"{g_logger.timestamp_str}_{label}"

    agent_a = CABTAgentWrapper(f"{label}_player_a", "skills", deck_a, g_logger, use_staging=use_staging_a)
    agent_b = CABTAgentWrapper(f"{label}_player_b", "skills", deck_b, g_logger, use_staging=use_staging_b)

    env = make("cabt")
    env.run([agent_a, agent_b])
    elapsed = time.time() - start_time

    for agent in [agent_a, agent_b]:
        try:
            if hasattr(agent, 'orchestrator'):
                agent.orchestrator.flush_all_logs()
        except Exception as e:
            logger.warning(f"Failed to flush orchestrator logs: {e}")

    p1_state, p2_state = env.steps[-1][0], env.steps[-1][1]
    winner = "player_a" if p1_state["reward"] == 1 else ("player_b" if p2_state["reward"] == 1 else "draw")

    prizes_a = prizes_b = 0
    try:
        players = p1_state.get("observation", {}).get("current", {}).get("players", [])
        if len(players) > 1:
            prizes_a = 6 - len(players[0].get("prize", []))
            prizes_b = 6 - len(players[1].get("prize", []))
    except:
        pass

    steps_dump = []
    for idx, step in enumerate(env.steps):
        step_data = []
        for player_idx, player_state in enumerate(step):
            clean_obs = {k: v for k, v in player_state.get("observation", {}).items() if k != "search_begin_input"}
            step_data.append({
                "player": player_idx, "action": player_state.get("action"),
                "reward": player_state.get("reward"), "status": player_state.get("status"),
                "observation": clean_obs
            })
        steps_dump.append({"step": idx, "players": step_data})

    prediction = "n/a"
    try:
        from factory.early_predictor import EarlyWinPredictor
        predictor = EarlyWinPredictor()
        prediction = predictor.predict_winner(deck_a, deck_b, steps_dump)
        if prediction != winner and winner in ("player_a", "player_b"):
            predictor.upgrade(prediction, winner, steps_dump)
    except Exception as e:
        logger.error(f"EarlyWinPredictor failed: {e}")

    g_logger.save(v_a, v_b)
    suffix = f"game_{g_logger.timestamp_str}_v{v_a}_vs_v{v_b}.json"

    return {
        "label": label, "winner": winner, "early_prediction": prediction, "turns_taken": len(env.steps),
        "prizes_taken_a": prizes_a, "prizes_taken_b": prizes_b, "time_elapsed": round(elapsed, 2),
        "timeout": (p1_state["status"] == "TIMEOUT" or p2_state["status"] == "TIMEOUT"),
        "log_files": {
            "action": f"action_{suffix}", "reasoning": f"reasoning_{suffix}",
            "variance": f"variance_{suffix}", "steps": f"steps_{label}_v{v_a}_vs_v{v_b}.json"
        },
        "steps_dump": steps_dump
    }
