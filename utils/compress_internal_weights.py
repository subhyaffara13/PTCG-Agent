
def compress_internal_weights(nus, regrets):
  """Compress internal weights.

  Via optimization, identify which regret timesteps are useful and which aren't
  for internal regret.

  Args:
    nus: Distribution per timestep.
    regrets: Regret value per timestep and action.

  Returns:
    Weights over nus which can be used to average the no-regret distribution.
  """

  def get_c(nus):
    return np.concatenate((np.array([1.0]), np.zeros(nus.shape[0])))

  def get_max_constraint(regrets):
    regrets = np.transpose(np.array(regrets), axes=[0, 2, 1])
    regrets = regrets.reshape(-1, regrets.shape[-1])
    A = np.zeros((regrets.shape[0], 1 + regrets.shape[1]))
    A[:, 1:] = regrets
    A[:, 0] = -1.0

    b = np.zeros(A.shape[0])
    return A, b

  def get_a_ub(nus, regrets):
    Amax, bmax = get_max_constraint(regrets)
    Apos, bpos = get_proba_constraints_positivity(nus)
    return np.concatenate((Amax, Apos), axis=0), np.concatenate(
        (bmax, bpos), axis=0
    )

  c = get_c(nus)

  A_ub, b_ub = get_a_ub(nus, regrets)
  A_eq, b_eq = get_proba_constraint_sum_eq(nus)

  res = scipy.optimize.linprog(
      c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, options={"tol": 1e-10}
  )
  new_weights = res.x
  return new_weights[1:]


def compress_internal_weights(nus, regrets, rewards, lbd=0.0):
  """Computes distribution over `nus` while minimizing internal regret.

  Args:
    nus: [T, P] array, T the number of different population distributions, P the
      number of different policies.
    regrets: [T, P, P] array, regrets[t, i, j] = payoff for switching from
      policy i to j at time t.
    rewards: [T, P] array, T the number of different population distributions, P
      the number of different policies
    lbd: Sparsity argument.

  Returns:
    Computed distribution over `nus`.
  """

  def get_c(nus):
    return np.concatenate(
        (np.array([1.0]), -lbd * np.sum(rewards * nus, axis=1))
    )

  def get_max_constraint(regrets):
    regrets = np.transpose(np.array(regrets), axes=[0, 2, 1])
    regrets = regrets.reshape(-1, regrets.shape[-1])
    A = np.zeros((regrets.shape[0], 1 + regrets.shape[1]))
    A[:, 1:] = regrets
    A[:, 0] = -1.0

    b = np.zeros(A.shape[0])
    return A, b

  def get_a_ub(nus, regrets):
    Amax, bmax = get_max_constraint(regrets)
    Apos, bpos = get_proba_constraints_positivity(nus)
    return np.concatenate((Amax, Apos), axis=0), np.concatenate(
        (bmax, bpos), axis=0
    )

  c = get_c(nus)

  A_ub, b_ub = get_a_ub(nus, regrets)
  A_eq, b_eq = get_proba_constraint_sum_eq(nus)

  res = scipy.optimize.linprog(
      c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, options={'tol': 1e-10}
  )
  new_weights = res.x
  return new_weights[1:]

