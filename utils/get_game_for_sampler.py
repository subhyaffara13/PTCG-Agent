
def get_game_for_sampler(game_name):
  """Returns pre-processed game data for ResponseGraphUCB examples."""
  # pylint: disable=invalid-name
  if game_name == 'bernoulli':
    M = get_payoffs_bernoulli_game()
    strategy_spaces = [2, 2]
    G = ZeroSumBernoulliGameSampler(
        strategy_spaces, means=M, payoff_bounds=[-1., 1.])
  elif game_name == 'soccer':
    M = get_soccer_data()
    M = M * 2. - 1  # Convert to zero-sum
    strategy_spaces = np.shape(M)
    M = np.asarray([M, M.T])
    G = ZeroSumBernoulliGameSampler(strategy_spaces, means=M,
                                    payoff_bounds=[np.min(M), np.max(M)])
  elif game_name in ['kuhn_poker_2p', 'kuhn_poker_3p', 'kuhn_poker_4p']:
    if '2p' in game_name:
      num_players = 2
    elif '3p' in game_name:
      num_players = 3
    elif '4p' in game_name:
      num_players = 4
    M = get_kuhn_poker_data(num_players, iterations=2)  # pylint: disable=invalid-name
    strategy_spaces = egt_utils.get_num_strats_per_population(M, False)
    G = BernoulliGameSampler(
        strategy_spaces, means=M, payoff_bounds=[np.min(M), np.max(M)])
  else:
    raise ValueError('Game', game_name, 'not implemented!')
  # pylint: enable=invalid-name
  return G

