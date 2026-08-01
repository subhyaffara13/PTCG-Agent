
def loss_gradients(dist, payoff_matrices, num_players, temperature=0.,
                   proj_grad=True):
  """Computes exploitablity gradient.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    payoff_matrices: 2 dictionaries with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
    temperature: non-negative float, default 0.
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist) as tuple
    unregularized exploitability (stochastic estimate)
    shannon regularized exploitability (stochastic estimate)
  """
  # first compute projected gradients (for every player, for each sample a & b)
  # if consulting paper https://arxiv.org/abs/2310.06689, code assumes eta_k = 1
  tau = temperature

  pgs = []
  for i in range(num_players):

    pg_i_a = np.zeros_like(dist[i])
    pg_i_b = np.zeros_like(dist[i])

    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij_a = payoff_matrices[0][(i, j)][0]
        hess_i_ij_b = payoff_matrices[1][(i, j)][0]
      else:
        hess_i_ij_a = payoff_matrices[0][(j, i)][1].T
        hess_i_ij_b = payoff_matrices[1][(j, i)][1].T

      pg_i_a_est = simplex.project_grad(hess_i_ij_a.dot(dist[j]))
      pg_i_b_est = simplex.project_grad(hess_i_ij_b.dot(dist[j]))

      pg_i_a += pg_i_a_est / float(num_players - 1)
      pg_i_b += pg_i_b_est / float(num_players - 1)

    pgs.append((pg_i_a, pg_i_b))

  # then construct unbiased stochastic gradient
  grad_dist = []
  unreg_exp = []
  reg_exp = []

  for i in range(num_players):

    grad_dist_i = np.zeros_like(dist[i])

    for j in range(num_players):
      pg_j_a = pgs[j][0]
      pg_j_b = pgs[j][1]
      if tau > 0.:
        log_dist_safe = np.clip(np.log(dist[j]), -40, 0)
        entr_grad_proj = simplex.project_grad(-tau * (log_dist_safe + 1))
      else:
        entr_grad_proj = 0.
      pg_j_a_entr = pg_j_a + entr_grad_proj
      pg_j_b_entr = pg_j_b + entr_grad_proj

      if j == i:
        if tau > 0.:
          hess_j_ij_a = -tau * np.diag(1. / dist[j])
        else:
          hess_j_ij_a = np.diag(np.zeros_like(dist[j]))
        unreg_exp_i = np.dot(pg_j_a, pg_j_b)
        reg_exp_i = np.dot(pg_j_a_entr, pg_j_b_entr)
        unreg_exp.append(unreg_exp_i)
        reg_exp.append(reg_exp_i)
      elif i < j:
        hess_j_ij_a = payoff_matrices[0][(i, j)][1]
      else:
        hess_j_ij_a = payoff_matrices[0][(j, i)][0].T

      grad_dist_i += 2. * hess_j_ij_a.dot(pg_j_b_entr)

    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)

    grad_dist.append(grad_dist_i)

  return (grad_dist,), np.mean(unreg_exp), np.mean(reg_exp)


def loss_gradients(dist, payoff_matrices, num_players, temperature=0.,
                   proj_grad=True):
  """Computes exploitablity gradient.

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    payoff_matrices: 2 (>=2 x A x A) np.arrays, payoffs for each joint action
    num_players: int, number of players, in case payoff_matrices is abbreviated
    temperature: non-negative float, default 0.
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist) as tuple
    unregularized exploitability (stochastic estimate)
    shannon regularized exploitability (stochastic estimate)
  """
  del num_players
  # if consulting paper https://arxiv.org/abs/2310.06689, code assumes eta = 1
  tau = temperature

  a, b = 0, 1  # 2 samples needed for unbiased estimation
  p_0, p_1 = 0, 1  # player 0 index, player 1 index
  hess_0_01_a = payoff_matrices[a][p_0]
  hess_1_01_a = payoff_matrices[a][p_1]
  hess_0_01_b = payoff_matrices[b][p_0]

  pg_0_a = simplex.project_grad(hess_0_01_a.dot(dist))
  pg_0_b = simplex.project_grad(hess_0_01_b.dot(dist))

  unreg_exp = np.dot(pg_0_a, pg_0_b)

  if tau > 0.:
    log_dist_safe = np.clip(np.log(dist), -40, 0)
    entr_grad_proj = simplex.project_grad(-tau * (log_dist_safe + 1))
  else:
    entr_grad_proj = 0.
  pg_0_a_entr = pg_0_a + entr_grad_proj
  pg_0_b_entr = pg_0_b + entr_grad_proj
  pg_0_entr = 0.5 * (pg_0_a_entr + pg_0_b_entr)
  pg_1_b_entr = pg_0_b_entr

  reg_exp = np.dot(pg_0_a_entr, pg_0_b_entr)

  # then construct unbiased stochastic gradient
  grad_dist = 2. * hess_1_01_a.dot(pg_1_b_entr)
  if tau > 0.:
    grad_dist += 2. * -tau * pg_0_entr / dist

  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)

  return (grad_dist,), unreg_exp, reg_exp

