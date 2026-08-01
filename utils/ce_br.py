
def ce_br(game, policies, weights, mus, nus, rewards=None):
  """Computes CE-BR.

  Args:
    game: Pyspiel MFG Game.
    policies: List of pyspiel policies, length P.
    weights: Array of temporal weights on each distribution in `nu`, length T.
    mus: List of state distributions, length T.
    nus: Array of policy distribution per timestep, shape (T, P)
    rewards: Optional array of policy reward per timestep, shape (T, P)

  Returns:
    Best-responses, computed exploitability from `rewards`.
  """
  assert len(mus) == len(nus)
  assert len(mus) == len(weights)

  policy_probability = np.sum(nus, axis=0)
  new_policies = []
  ce_gap_value = 0.0
  nus = np.array(nus)
  weights = np.array(weights)
  for policy_index in range(len(policies)):
    if policy_probability[policy_index] > 0:
      # Take conditional distribution
      pol_weights = nus[:, policy_index] * weights
      pol_proba = np.sum(pol_weights)
      pol_weights = pol_weights / pol_proba

      # Prune state distribution and weights from 0.0-weightred values
      new_mus = [mu for ind, mu in enumerate(mus) if pol_weights[ind] > 0]
      new_weights = np.array([
          weight for ind, weight in enumerate(pol_weights)
          if pol_weights[ind] > 0
      ])

      # Compute best-response.
      new_pol, new_val = get_joint_br(game, new_weights, new_mus)
      new_br_val = new_val.value(game.new_initial_states()[0])

      # Evaluate CE-Gap
      if len(rewards) > 0:  # pylint: disable=g-explicit-length-test
        on_policy_value = np.sum(
            np.array(rewards)[:, policy_index] * pol_weights)
        ce_gap_value += pol_proba * (new_br_val - on_policy_value)
      new_policies.append(new_pol)
  return new_policies, ce_gap_value

