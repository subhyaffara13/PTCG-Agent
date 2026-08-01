
def update_observations_and_rewards(configuration, state, obs, rew=None):
    """Updates agent-visible observations given 'raw' observations from environment.
    Observations in 'obs' are coming directly from the environment and are in 'raw' format.
    """
    state[0].observation.controlled_players = configuration.team_1
    state[1].observation.controlled_players = configuration.team_2

    assert len(obs) == configuration.team_1 + configuration.team_2
    if rew is not None:
        state[0].reward = rew
        state[1].reward = -rew
    state[0].observation.players_raw = [parse_single_player(obs[x]) for x in range(configuration.team_1)]
    state[1].observation.players_raw = [
        parse_single_player(obs[x + configuration.team_1]) for x in range(configuration.team_2)
    ]

