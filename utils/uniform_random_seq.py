
def uniform_random_seq(game, infoset_actions_to_seq):
  """Generate uniform random sequence.

  The sequence generated is equivalent to a uniform random tabular policy.

  Args:
      game: the spiel game to solve (must be zero-sum, sequential, and have
        chance mode of deterministic or explicit stochastic).
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id.

  Returns:
      A list of NumPy arrays, one for each player.
  """
  policies = policy.TabularPolicy(game)
  initial_state = game.new_initial_state()
  sequences = [
      np.ones(len(infoset_actions_to_seq[i])) for i in range(game.num_players())
  ]
  _policy_to_sequence(
      initial_state,
      policies,
      sequences,
      infoset_actions_to_seq,
      [1 for _ in range(game.num_players())],
  )
  return sequences

