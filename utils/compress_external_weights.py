
def compress_external_weights(nus, regrets, lbd=0.0):
  """Compress internal weights.

  Via optimization, identify which regret timesteps are useful and which aren't
  for external regret.

  Args:
    nus: Distribution per timestep.
    regrets: Regret value per timestep and action.
    lbd: Sparsity penalty.

  Returns:
    Weights over nus which can be used to average the no-regret distribution.
  """

  def get_c(nus):
    return np.concatenate((np.array([1.0]), np.zeros(nus.shape[0])))

  def get_max_constraints(nus, regrets, lbd):
    A = np.zeros((regrets.shape[1], 1 + nus.shape[0]))
    A[:, 0] = -1.0
    A[:, 1:] = np.transpose(
        regrets
        - np.sum(regrets * nus, axis=1).reshape(-1, 1)
        - lbd * np.abs(regrets)
    )
    return A, np.zeros(A.shape[0])

  def get_a_ub(nus, regrets, lbd):
    Amax, bmax = get_max_constraints(nus, regrets, lbd)
    Apos, bpos = get_proba_constraints_positivity(nus)
    return np.concatenate((Amax, Apos), axis=0), np.concatenate(
        (bmax, bpos), axis=0
    )

  c = get_c(nus)

  A_ub, b_ub = get_a_ub(nus, regrets, lbd)
  A_eq, b_eq = get_proba_constraint_sum_eq(nus)

  res = scipy.optimize.linprog(
      c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, options={"tol": 1e-10}
  )
  new_weights = res.x
  return new_weights[1:]


def compress_external_weights(nus, regrets, rewards, lbd=0.0):
  """Computes distribution over `nus` while minimizing external regret.

  Args:
    nus: [T, P] array, T the number of different population distributions, P the
      number of different policies.
    regrets: [T, P] array, regrets[t, i] = payoff for switching from current
      policy to i at time t.
    rewards: [T, P] array, reward for playing policy P at time T.
    lbd: Sparsity argument.

  Returns:
    Computed distribution over `nus`.
  """

  def get_c(nus):
    return np.concatenate(
        (np.array([1.0]), -lbd * np.sum(rewards * nus, axis=1))
    )

  def get_max_constraints(nus, regrets, lbd):
    A = np.zeros((regrets.shape[1], 1 + nus.shape[0]))
    A[:, 0] = -1.0
    A[:, 1:] = np.transpose(
        regrets
        - np.sum(regrets * nus, axis=1).reshape(-1, 1)
        - lbd * np.abs(regrets)
    )
    return A, np.zeros(A.shape[0])

  def get_a_ub(nus, regrets, lbd):
    Amax, bmax = get_max_constraints(nus, regrets, lbd)
    Apos, bpos = get_proba_constraints_positivity(nus)
    return np.concatenate((Amax, Apos), axis=0), np.concatenate(
        (bmax, bpos), axis=0
    )

  c = get_c(nus)

  A_ub, b_ub = get_a_ub(nus, regrets, lbd)
  A_eq, b_eq = get_proba_constraint_sum_eq(nus)

  res = scipy.optimize.linprog(
      c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, options={'tol': 1e-10}
  )
  new_weights = res.x
  return new_weights[1:]

