
def get_tabular_policy_states(game):
  """Returns the states of the game for a tabular policy."""
  if game.get_type().dynamics == pyspiel.GameType.Dynamics.MEAN_FIELD:
    # TODO(author18): We use s.observation_string(DEFAULT_MFG_PLAYER) here as the
    # number of history is exponential on the depth of the MFG. What we really
    # need is a representation of the state. For many player Mean Field games,
    # the state will be (x0, x1, x2, ..., xn) and the observation_string(0) will
    # output the string of x0. In that case we would need something like
    # str([observation_string(i) for i in range(num_player)])
    to_string = lambda s: s.observation_string(pyspiel.PlayerId.
                                               DEFAULT_PLAYER_ID)
  else:
    to_string = lambda s: s.history_str()
  return get_all_states.get_all_states(
      game,
      depth_limit=-1,
      include_terminals=False,
      include_chance_states=False,
      include_mean_field_states=False,
      to_string=to_string)

