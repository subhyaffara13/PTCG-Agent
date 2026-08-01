
def _cce_constraints(payoff, epsilons, remove_null=True, zero_tolerance=1e-8):
  """Returns the coarse correlated constraints.

  Args:
    payoff: A [NUM_PLAYER, NUM_ACT_0, NUM_ACT_1, ...] shape payoff tensor.
    epsilons: Per player floats corresponding to the epsilon.
    remove_null: Remove null rows of the constraint matrix.
    zero_tolerance: Zero out elements with small value.

  Returns:
    a_mat: The gain matrix for deviting to an action or shape [SUM(A), PROD(A)].
    meta: Dictionary containing meta information.
  """
  num_players = payoff.shape[0]
  num_actions = payoff.shape[1:]
  num_dists = int(np.prod(num_actions))

  cor_cons = int(np.sum(num_actions))

  a_mat = np.zeros([cor_cons] + list(num_actions))
  p_vec = np.zeros([cor_cons], dtype=np.int32)
  i_vec = np.zeros([cor_cons], dtype=np.int32)
  con = 0
  for p in range(num_players):
    for a1 in range(num_actions[p]):
      a1_inds = tuple(_indices(p, a1, num_players))
      for a0 in range(num_actions[p]):
        a0_inds = tuple(_indices(p, a0, num_players))
        a_mat[con][a0_inds] += payoff[p][a1_inds]
      a_mat[con] -= payoff[p]
      a_mat[con] -= epsilons[p]

      p_vec[con] = p
      i_vec[con] = a0

      con += 1

  a_mat = np.reshape(a_mat, [cor_cons, num_dists])
  a_mat[np.abs(a_mat) < zero_tolerance] = 0.0
  if remove_null:
    null_cons = np.any(a_mat != 0.0, axis=-1)
    redundant_cons = np.max(a_mat, axis=1) >= 0
    nonzero_mask = null_cons & redundant_cons
    a_mat = a_mat[nonzero_mask, :].copy()
    p_vec = p_vec[nonzero_mask].copy()
    i_vec = i_vec[nonzero_mask].copy()

  meta = dict(
      p_vec=p_vec,
      i_vec=i_vec,
      epsilons=epsilons,
  )

  return a_mat, meta

