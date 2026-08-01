
def get_raw_observation(kaggle_observation) -> WerewolfObservationModel:
    """

    Args:
        kaggle_observation:

    Returns: a dict of WerewolfObservationModel dump
    """
    return WerewolfObservationModel(**kaggle_observation[ObsKeys.RAW_OBSERVATION])

