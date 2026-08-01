
def _game_type(game_type: pyspiel.GameType, **overrides) -> pyspiel.GameType:
    """Returns a GameType with the given overrides."""
    kwargs = dict(
        short_name=game_type.short_name,
        long_name=game_type.long_name,
        dynamics=game_type.dynamics,
        chance_mode=game_type.chance_mode,
        information=game_type.information,
        utility=game_type.utility,
        reward_model=game_type.reward_model,
        max_num_players=game_type.max_num_players,
        min_num_players=game_type.min_num_players,
        provides_information_state_string=game_type.provides_information_state_string,
        provides_information_state_tensor=game_type.provides_information_state_tensor,
        provides_observation_string=game_type.provides_observation_string,
        provides_observation_tensor=game_type.provides_observation_tensor,
        parameter_specification=game_type.parameter_specification,
        default_loadable=game_type.default_loadable,
        provides_factored_observation_string=game_type.provides_factored_observation_string,
    )
    kwargs.update(**overrides)
    return pyspiel.GameType(**kwargs)

