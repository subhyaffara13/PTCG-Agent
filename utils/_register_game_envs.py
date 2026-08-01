
def _register_game_envs(games_list: list[str]) -> dict[str, Any]:
    skipped_games = []
    registered_envs = {}
    for game_string in games_list:
        try:
            env_config = _build_env(game_string)
            if env_config is None:
                continue
            env_name = env_config["specification"]["name"]
            if env_name in registered_envs:
                raise ValueError(f"Attempting to overwrite existing env: {env_name}")
            registered_envs[env_name] = env_config
        except Exception as e:  # pylint: disable=broad-exception-caught
            _log.debug(e)
            skipped_games.append(game_string)

    _log.info(f"Successfully loaded OpenSpiel environments: {len(registered_envs)}.")
    for env_name in registered_envs:
        _log.info(f"   {env_name}")
    _log.info(f"OpenSpiel games skipped: {len(skipped_games)}.")
    for game_string in skipped_games:
        _log.info(f"   {game_string}")

    return registered_envs

