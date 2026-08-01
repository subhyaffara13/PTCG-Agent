
def set_raw_observation(kaggle_player_state, raw_obs: WerewolfObservationModel):
    """Persist raw observations for players in kaggle's player state

    Args:
        kaggle_player_state: Kaggle's interpreter state is a list of player state. This arg is one player state item.
        raw_obs: the raw observation for a player extracted from game engine.

    Note: using raw_obs.model_dump_json() will greatly increase rendering speed (due to kaggle environment's use
        of deepcopy for serialization) at the expense of harder to parse JSON rendering, since we are getting a json
        string instead of human-readable dump. We choose raw_obs.model_dump() for clarity.
    """
    kaggle_player_state.observation[ObsKeys.RAW_OBSERVATION] = raw_obs.model_dump()

