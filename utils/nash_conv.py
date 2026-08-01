
def nash_conv(game, policy, return_only_nash_conv=True, use_cpp_br=False):
  r"""Returns a measure of closeness to Nash for a policy in the game.

  See https://arxiv.org/pdf/1711.00832.pdf for the NashConv definition.

  Args:
    game: An open_spiel game, e.g. kuhn_poker
    policy: A `policy.Policy` object. This policy should depend only on the
      information state available to the current player, but this is not
      enforced.
    return_only_nash_conv: Whether to only return the NashConv value, or a
      namedtuple containing additional statistics. Prefer using `False`, as we
      hope to change the default to that value.
    use_cpp_br: if True, compute the best response in c++

  Returns:
    Returns a object with the following attributes:
    - player_improvements: A `[num_players]` numpy array of the improvement
      for players (i.e. value_player_p_versus_BR - value_player_p).
    - nash_conv: The sum over all players of the improvements in value that each
      player could obtain by unilaterally changing their strategy, i.e.
      sum(player_improvements).
  """
  root_state = game.new_initial_state()
  if use_cpp_br:
    best_response_values = np.array([
        pyspiel_best_response.CPPBestResponsePolicy(
            game, best_responder, policy).value(root_state)
        for best_responder in range(game.num_players())
    ])
  else:
    best_response_values = np.array([
        pyspiel_best_response.BestResponsePolicy(
            game, best_responder, policy).value(root_state)
        for best_responder in range(game.num_players())
    ])
  on_policy_values = _state_values(root_state, game.num_players(), policy)
  player_improvements = best_response_values - on_policy_values
  nash_conv_ = sum(player_improvements)
  if return_only_nash_conv:
    return nash_conv_
  else:
    return _NashConvReturn(
        nash_conv=nash_conv_, player_improvements=player_improvements)

