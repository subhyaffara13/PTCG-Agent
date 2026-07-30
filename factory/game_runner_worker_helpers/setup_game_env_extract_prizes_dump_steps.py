from . import Path, os, sys
from .dummystream_silence_kaggle_warnings import silence_kaggle_warnings

def setup_game_env(seed=None):
    os.environ.pop("FAST_SIM_MODE", None)  # Ensure C++ ptcg_core acceleration is fully enabled
    os.environ["SKIP_GAME_LOGS"] = "1"
    saved_path = list(sys.path)
    try:
        cwd_resolved = Path.cwd().resolve()
        sys.path = [p for p in sys.path if p and Path(p).resolve() != cwd_resolved]
        
        # Suppress prints and stderr messages from kaggle_environments cleanly
        with silence_kaggle_warnings():
            from kaggle_environments import make
            # Inject strict Kaggle execution limits to simulate leaderboard environment
            config = {
                "actTimeout": 1.5,
                "runTimeout": 300,
                "episodeSteps": 500
            }
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

