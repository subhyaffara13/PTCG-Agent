
def cce_br(game, policies, weights, mus, nus, rewards=None):
  """Computes CCE-BR.

  Args:
    game: Pyspiel MFG Game.
    policies: List of pyspiel policies, length P.
    weights: Array of temporal weights on each distribution in `nu`, length T.
    mus: List of state distributions, length T.
    nus: Array of policy distribution per timestep, shape (T, P)
    rewards: Optional array of policy reward per timestep, shape (T, P)

  Returns:
    Best-response, computed exploitability from `rewards`.
  """
  assert len(mus) == len(nus)
  assert len(mus) == len(weights)

  del policies
  pol, val = get_joint_br(game, weights, mus)
  cce_gap_value = None
  if len(rewards) > 0:  # pylint: disable=g-explicit-length-test
    deviation_value = val.value(game.new_initial_states()[0])
    on_policy_value = np.sum(weights * np.sum(rewards * nus, axis=1))
    cce_gap_value = deviation_value - on_policy_value
  return [pol], cce_gap_value

