
def make_observation(
    game,
    imperfect_information_observation_type=None,
    params=None,
):
  """Make an observation.

  Args:
    game: a pyspiel.Game object.
    imperfect_information_observation_type: an IIGObservationType object.
    params: game-specific parameters for observations.

  Returns:
    An _Observation instance if the
    imperfect_information_observation_type is supported, otherwise None.
  """
  params = params or {}
  if hasattr(game, 'make_py_observer'):
    return game.make_py_observer(imperfect_information_observation_type, params)
  else:
    if imperfect_information_observation_type is not None:
      observer = game.make_observer(
          imperfect_information_observation_type, params
      )
    else:
      observer = game.make_observer(params)
    if observer is None:
      return None
    return _Observation(game, observer)


def make_observation(
    game,
    imperfect_information_observation_type=None,
    params=None,
):
    """Returns an _Observation instance if the imperfect_information_observation_type is supported, otherwise None."""
    params = params or {}
    if hasattr(game, "make_py_observer"):
        return game.make_py_observer(imperfect_information_observation_type, params)
    else:
        if imperfect_information_observation_type is not None:
            observer = game.make_observer(imperfect_information_observation_type, params)
        else:
            observer = game.make_observer(params)
        if observer is None:
            return None
        return _Observation(game, observer)

