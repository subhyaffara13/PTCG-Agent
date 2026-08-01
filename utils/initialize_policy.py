
def initialize_policy(game, player, policy_init):
  """Returns initial policy."""
  if policy_init == "uniform":
    new_policy = policy.TabularPolicy(game, players=(player,))

  elif policy_init == "random_deterministic":
    new_policy = policy.TabularPolicy(game, players=(player,))
    for i in range(new_policy.action_probability_array.shape[0]):
      new_policy.action_probability_array[i] = np.random.multinomial(
          1, new_policy.action_probability_array[i]).astype(np.float64)

  else:
    raise ValueError(
        "policy_init must be a valid initialization strategy: %s. "
        "Received: %s" % (INIT_POLICIES, policy_init))

  return new_policy

