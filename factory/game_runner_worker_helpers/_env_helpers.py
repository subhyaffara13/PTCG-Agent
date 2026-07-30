def _build_env_config(seed):
    config = {"actTimeout": 1.5, "runTimeout": 300, "episodeSteps": 500}
    if seed is not None: config["seed"] = seed
    return config
