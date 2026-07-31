def _build_env_config(seed):
    config = {"actTimeout": 2.0, "runTimeout": 600, "episodeSteps": 100}
    if seed is not None: config["seed"] = seed
    return config
