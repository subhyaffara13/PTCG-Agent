
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
                "actTimeout": 2.0,
                "runTimeout": 600,
                "episodeSteps": 1000
            }
            if seed is not None:
                config["seed"] = seed
            env = make("cabt", configuration=config)
    finally:
        sys.path = saved_path
    return env

