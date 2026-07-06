import time
import logging
from pathlib import Path
from factory.game_logger import GameLogger
from factory.game_agent_wrapper import CABTAgentWrapper
from factory.game_runner_worker_helpers import setup_game_env, extract_prizes, dump_steps, run_early_prediction, write_steps_file

logger = logging.getLogger(__name__)

def _parallel_game_worker(log_dir: str, label: str, v_a: str, v_b: str, 
                          deck_a: list[int], deck_b: list[int], use_staging_a: bool, use_staging_b: bool, seed: int | None = None) -> dict:
    env = setup_game_env(seed)

    start_time = time.time()
    g_logger = GameLogger(log_dir=log_dir)
    g_logger.timestamp_str = f"{g_logger.timestamp_str}_{label}"

    agent_a = CABTAgentWrapper(f"{label}_player_a", "skills", deck_a, g_logger, use_staging=use_staging_a)
    agent_b = CABTAgentWrapper(f"{label}_player_b", "skills", deck_b, g_logger, use_staging=use_staging_b)

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

    prizes_a, prizes_b = extract_prizes(p1_state, p2_state)
    steps_dump = dump_steps(env.steps)
    prediction = run_early_prediction(deck_a, deck_b, steps_dump, winner)

    g_logger.save(v_a, v_b)
    suffix = f"game_{g_logger.timestamp_str}_v{v_a}_vs_v{v_b}.json"
    steps_filename = write_steps_file(log_dir, g_logger.timestamp_str, label, v_a, v_b, steps_dump)

    return {
        "label": label, "winner": winner, "early_prediction": prediction, "turns_taken": len(env.steps),
        "prizes_taken_a": prizes_a, "prizes_taken_b": prizes_b, "time_elapsed": round(elapsed, 2),
        "timeout": (p1_state["status"] == "TIMEOUT" or p2_state["status"] == "TIMEOUT"),
        "log_files": {
            "action": f"action_{suffix}", "reasoning": f"reasoning_{suffix}",
            "variance": f"variance_{suffix}", "steps": steps_filename
        },
    }
