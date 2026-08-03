import itertools

def _ace_constraints(payoff, epsilons, remove_null=True, zero_tolerance=0.0):
  """Returns sparse alternate ce constraints Ax - epsilon <= 0.

  Args:
    payoff: Dense payoff tensor.
    epsilons: Scalar epsilon approximation.
    remove_null: Whether to remove null row constraints.
    zero_tolerance: Smallest absolute value.

  Returns:
    a_csr: Sparse gain matrix from switching from one action to another.
    e_vec: Epsilon vector.
    meta: Dictionary containing meta information.
  """
  num_players = payoff.shape[0]
  num_actions = payoff.shape[1:]
  num_dists = int(np.prod(num_actions))

  num_cons = 0
  for p in range(num_players):
    num_cons += num_actions[p] * (num_actions[p] - 1)

  a_dok = sp.sparse.dok_matrix((num_cons, num_dists))
  e_vec = np.zeros([num_cons])
  p_vec = np.zeros([num_cons], dtype=np.int32)
  i_vec = np.zeros([num_cons, 2], dtype=np.int32)

  num_null_cons = None
  num_redundant_cons = None
  num_removed_cons = None

  if num_cons > 0:
    con = 0
    for p in range(num_players):
      generator = itertools.permutations(range(num_actions[p]), 2)
      for a0, a1 in generator:
        a0_inds = _sparse_indices_generator(p, a0, num_actions)
        a1_inds = _sparse_indices_generator(p, a1, num_actions)

        for a0_ind, a1_ind in zip(a0_inds, a1_inds):
          a0_ind_flat = np.ravel_multi_index(a0_ind, num_actions)
          val = payoff[p][a1_ind] - payoff[p][a0_ind]
          if abs(val) > zero_tolerance:
            a_dok[con, a0_ind_flat] = val

        e_vec[con] = epsilons[p]
        p_vec[con] = p
        i_vec[con] = [a0, a1]
        con += 1

    a_csr = a_dok.tocsr()
    if remove_null:
      null_cons = np.logical_or(
          a_csr.max(axis=1).todense() != 0.0,
          a_csr.min(axis=1).todense() != 0.0)
      null_cons = np.ravel(null_cons)
      redundant_cons = np.ravel(a_csr.max(axis=1).todense()) >= e_vec
      nonzero_mask = null_cons & redundant_cons
      a_csr = a_csr[nonzero_mask, :]
      e_vec = e_vec[nonzero_mask].copy()
      p_vec = p_vec[nonzero_mask].copy()
      i_vec = i_vec[nonzero_mask].copy()
      num_null_cons = np.sum(~null_cons)
      num_redundant_cons = np.sum(~redundant_cons)
      num_removed_cons = np.sum(~nonzero_mask)

  else:
    a_csr = a_dok.tocsr()

  meta = dict(
      p_vec=p_vec,
      i_vec=i_vec,
      epsilons=epsilons,
      num_null_cons=num_null_cons,
      num_redundant_cons=num_redundant_cons,
      num_removed_cons=num_removed_cons,
  )

  return a_csr, e_vec, meta

