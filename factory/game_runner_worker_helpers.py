import os
import sys
import json
import time
import contextlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DummyStream:
    def write(self, s):
        pass
    def flush(self):
        pass

@contextlib.contextmanager
def silence_kaggle_warnings():
    import builtins
    orig_print = builtins.print
    def dummy_print(*args, **kwargs):
        if args and isinstance(args[0], str) and ("Loading environment" in args[0] and "failed" in args[0]):
            return
        orig_print(*args, **kwargs)
    builtins.print = dummy_print
    
    dummy_stream = DummyStream()
    try:
        with contextlib.redirect_stderr(dummy_stream), contextlib.redirect_stdout(dummy_stream):
            yield
    finally:
        builtins.print = orig_print

def setup_game_env(seed=None):
    os.environ["FAST_SIM_MODE"] = "false"
    saved_path = list(sys.path)
    try:
        cwd_resolved = Path.cwd().resolve()
        sys.path = [p for p in sys.path if p and Path(p).resolve() != cwd_resolved]
        
        # Suppress prints and stderr messages from kaggle_environments cleanly
        with silence_kaggle_warnings():
            from kaggle_environments import make
            config = {}
            if seed is not None:
                config["seed"] = seed
            env = make("cabt", configuration=config)
    finally:
        sys.path = saved_path
    return env


def extract_prizes(p1_state: dict, p2_state: dict) -> tuple:
    prizes_a = prizes_b = 0
    try:
        players = p1_state.get("observation", {}).get("current", {}).get("players", [])
        if len(players) > 1:
            prizes_a = 6 - len(players[0].get("prize", []))
            prizes_b = 6 - len(players[1].get("prize", []))
    except Exception:
        pass
    return prizes_a, prizes_b


def dump_steps(raw_steps: list) -> list:
    steps_dump = []
    for idx, step in enumerate(raw_steps or []):
        step_data = []
        for player_idx, player_state in enumerate(step or []):
            if player_state is None:
                player_state = {}
            clean_obs = {k: v for k, v in player_state.get("observation", {}).items() if k != "search_begin_input"}
            step_data.append({
                "action": player_state.get("action"),
                "reward": player_state.get("reward"),
                "status": player_state.get("status"),
                "observation": clean_obs
            })
        steps_dump.append(step_data)
    return steps_dump


def run_early_prediction(deck_a: list, deck_b: list, steps_dump: list, winner: str) -> str:
    prediction = "n/a"
    try:
        from factory.early_predictor import EarlyWinPredictor
        predictor = EarlyWinPredictor()
        prediction = predictor.predict_winner(deck_a, deck_b, steps_dump)
        if os.environ.get("IS_WORKER") != "true":
            if prediction != winner and winner in ("player_a", "player_b"):
                predictor.upgrade(prediction, winner, steps_dump)
    except Exception as e:
        logger.error(f"EarlyWinPredictor failed: {e}")
    return prediction


def write_steps_file(log_dir: str, timestamp_str: str, label: str, v_a: str, v_b: str, steps_dump: list):
    steps_filename = f"steps_{timestamp_str}_{label}_v{v_a}_vs_v{v_b}.json"
    steps_path = Path(log_dir) / steps_filename
    
    final_rewards = [0.0, 0.0]
    if steps_dump and len(steps_dump[-1]) >= 2:
        final_rewards = [
            steps_dump[-1][0].get("reward") or 0.0,
            steps_dump[-1][1].get("reward") or 0.0
        ]
        
    replay_data = {
        "steps": steps_dump,
        "rewards": final_rewards,
        "info": {
            "TeamNames": [v_a, v_b]
        }
    }
    
    try:
        steps_path.write_text(json.dumps(replay_data, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to write steps file {steps_path}: {e}")
    return steps_filename
