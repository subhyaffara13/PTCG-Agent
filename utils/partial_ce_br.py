
def partial_ce_br(game, policies, weights, mus, nus, rewards=None):
  """Computes CE-BR for a single sampled policy.

  Args:
    game: Pyspiel MFG Game.
    policies: List of pyspiel policies, length P.
    weights: Array of temporal weights on each distribution in `nu`, length T.
    mus: List of state distributions, length T.
    nus: Array of policy distribution per timestep, shape (T, P)
    rewards: Optional array of policy reward per timestep, shape (T, P)

  Returns:
    Best-response, noisy exploitability estimation.
  """
  policy_probability = np.sum(nus, axis=0)
  new_policies = []

  ce_gap_value = None
  policy_index = np.random.choice(list(range(len(policies))))
  if policy_probability[policy_index] > 0:
    # Take conditional distribution
    pol_weights = [nu[policy_index] * weight for nu, weight in zip(
        nus, weights)]
    pol_proba = np.sum(pol_weights)
    pol_weights = np.array(pol_weights) / pol_proba

    # Prune state distribution and weights from 0.0-weightred values
    new_mus = [mu for ind, mu in enumerate(mus) if pol_weights[ind] > 0]
    new_weights = [
        weight for ind, weight in enumerate(pol_weights)
        if pol_weights[ind] > 0
    ]

    # Compute best-response.
    new_pol, new_val = get_joint_br(game, new_weights, new_mus)
    new_br_val = new_val.value(game.new_initial_states()[0])

    # Evaluate CE-Gap
    if len(rewards) > 0:  # pylint: disable=g-explicit-length-test
      on_policy_value = np.sum(np.array(rewards)[:, policy_index] * pol_weights)
      ce_gap_value = (new_br_val - on_policy_value)
    new_policies.append(new_pol)
  return new_policies, ce_gap_value

