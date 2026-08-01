
def run_games_and_record_payoffs(game_queries, evaluate_game, ckpt_to_policy):
  """Simulate games according to game queries and return results.

  Args:
    game_queries: set of tuples containing indices specifying each players strat
      key_query = (agent_tuple, profile_tuple) format
    evaluate_game: callable function that takes a list of policies as argument
    ckpt_to_policy: list of maps from strat (or checkpoint) to a policy, one
      map for each player
  Returns:
    dictionary: key=key_query, value=np.array of payoffs (1 for each player)
  """
  game_results = {}
  for key_query in game_queries:
    _, query = key_query
    policies = [ckpt_to_policy[pi][ckpt_i] for pi, ckpt_i in enumerate(query)]
    payoffs = evaluate_game(policies)
    game_results.update({key_query: payoffs})
  return game_results


def run_games_and_record_payoffs(game_queries, evaluate_game, ckpt_to_policy):
  """Simulate games according to game queries and return results.

  Args:
    game_queries: set of tuples containing indices specifying each players strat
    evaluate_game: callable function that takes a list of policies as argument
    ckpt_to_policy: maps a strat (or checkpoint) to a policy
  Returns:
    dictionary: key=query, value=np.array of payoffs (1 for each player)
  """
  game_results = {}
  for query in game_queries:
    policies = [ckpt_to_policy[ckpt] for ckpt in query]
    payoffs = evaluate_game(policies)
    game_results.update({query: payoffs})
  return game_results

