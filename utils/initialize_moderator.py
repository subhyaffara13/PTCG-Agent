
def initialize_moderator(state, env):
    num_players = len(state)

    agents_from_config = env.configuration.agents

    if env.info.get("Agents"):
        inject_kaggle_scheduler_info(agents_from_config, env)

    # below checks for configuration consistency with agent count. If inconsistent, it will cause down stream subtle error.
    if len(agents_from_config) < num_players:
        raise ValueError(
            f"Configuration has {len(agents_from_config)} agents, but {num_players} kaggle agents are present."
        )

    players = create_players_from_agents_config(
        agents_from_config,
        randomize_roles=env.configuration.randomize_roles,
        randomize_ids=env.configuration.randomize_ids,
        seed=env.configuration.seed,
    )

    env.game_state = GameState(
        players=players,
        history={},
        night_elimination_reveal_level=env.configuration.night_elimination_reveal_level,
        day_exile_reveal_level=env.configuration.day_exile_reveal_level,
    )

    env.player_ids_map = {i: p.id for i, p in enumerate(players)}
    env.player_id_str_list = [p.id for p in players]

    env.player_thumbnails = {p.id: p.agent.thumbnail for p in players}
    # Initialize protocols from configuration or defaults
    discussion_protocol = create_protocol(
        env.configuration.get("discussion_protocol", {}), default_name=DEFAULT_DISCUSSION_PROTOCOL_NAME
    )
    day_voting_protocol = create_protocol(
        env.configuration.get("day_voting_protocol", {}), default_name=DEFAULT_VOTING_PROTOCOL_NAME
    )
    night_voting_protocol = create_protocol(
        env.configuration.get("werewolf_night_vote_protocol", {}), default_name=DEFAULT_VOTING_PROTOCOL_NAME
    )

    logger.info(
        f"Interpreter: Using Discussion: {type(discussion_protocol).__name__}, "
        f"Day Voting: {type(day_voting_protocol).__name__}, "
        f"Night WW Voting: {type(night_voting_protocol).__name__}"
    )

    env.moderator = Moderator(
        state=env.game_state,
        discussion=discussion_protocol,
        day_voting=day_voting_protocol,
        night_voting=night_voting_protocol,
        night_elimination_reveal_level=env.configuration.night_elimination_reveal_level,
        day_exile_reveal_level=env.configuration.day_exile_reveal_level,
    )

    env.player_full_visible_history_cache = {p_id: [] for p_id in env.player_id_str_list}
    env.info[EnvInfoKeys.MODERATOR_OBS] = []
    env.agents = agents

