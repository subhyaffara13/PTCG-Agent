
def _init_game(config, seed=None):
    """Create a new GameState from the Kaggle configuration.

    If ``mapName`` is set and matches a built-in, that map is used. Otherwise
    ``seed`` deterministically selects a map from BUILTIN_MAPS (sorted by name).
    The chosen map then gets small seed-driven, point-symmetric terrain flips
    so no two episodes play on an identical layout.
    """
    map_name = getattr(config, "mapName", "")

    if not map_name or map_name not in BUILTIN_MAPS:
        map_name = _select_map_by_seed(seed)

    map_rows = _mutate_map(BUILTIN_MAPS[map_name], seed)
    map_data = _pad_map(map_rows)

    enabled_units = [u.strip() for u in config.enabledUnits.split(",") if u.strip()]

    game = GameState(
        map_data,
        num_players=2,
        max_turns=config.episodeSteps,
        enabled_units=enabled_units,
        engine_overrides=ENGINE_OVERRIDES,
    )

    # Override starting gold if configured
    starting_gold = config.startingGold
    game.player_gold = {1: starting_gold, 2: starting_gold}

    return game

