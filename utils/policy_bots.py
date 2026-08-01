
def policy_bots():
  random_policy = policy.UniformRandomPolicy(GAME)

  py_bot = PolicyBot(0, np.random.RandomState(4321), random_policy)
  cpp_bot = pyspiel.make_policy_bot(
      GAME, 1, 1234,
      policy.python_policy_to_pyspiel_policy(random_policy.to_tabular()))

  return [py_bot, cpp_bot]

