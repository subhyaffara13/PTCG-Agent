def _build_env_config(seed):
    config = {"actTimeout": 2.0, "runTimeout": 300, "episodeSteps": 250}
    if seed is not None: config["seed"] = seed
    return config
