
def init_br_responder(env):
  """Initializes the tabular best-response based responder and agents."""
  random_policy = policy.TabularPolicy(env.game)
  oracle = best_response_oracle.BestResponseOracle(
      game=env.game, policy=random_policy)
  agents = [random_policy.__copy__() for _ in range(FLAGS.n_players)]
  return oracle, agents

