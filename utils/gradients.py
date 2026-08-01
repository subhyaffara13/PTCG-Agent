
def gradients(dist, payoff_matrices, num_players, temperature=0.,
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


def gradients(dist, y, payoff_matrices, num_players, p=1, proj_grad=True):
  """Computes exploitablity gradient and aux variable gradients.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    y: list 1-d np.arrays (same shape as dist), current est. of payoff gradient
    payoff_matrices: dictionary with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
    p: float in [0, 1], Tsallis entropy-regularization --> 0 as p --> 0
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
  # first compute policy gradients and player effects (fx)
  policy_gradient = []
  other_player_fx = []
  grad_y = []
  unreg_exp = []
  reg_exp = []
  for i in range(num_players):

    nabla_i = np.zeros_like(dist[i])
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij = payoff_matrices[(i, j)][0]
      else:
        hess_i_ij = payoff_matrices[(j, i)][1].T

      nabla_ij = hess_i_ij.dot(dist[j])
      nabla_i += nabla_ij / float(num_players - 1)

    grad_y.append(y[i] - nabla_i)

    if p > 0:
      power = 1. / float(p)
      s_i = np.linalg.norm(y[i], ord=power)
      if s_i == 0:
        br_i = misc.uniform_dist(y[i])
      else:
        br_i = (y[i] / s_i)**power
    else:
      power = np.inf
      s_i = np.linalg.norm(y[i], ord=power)
      br_i = np.zeros_like(dist[i])
      maxima_i = (y[i] == s_i)
      br_i[maxima_i] = 1. / maxima_i.sum()

    policy_gradient_i = nabla_i - s_i * dist[i]**p
    policy_gradient.append(policy_gradient_i)

    unreg_exp.append(np.max(y[i]) - y[i].dot(dist[i]))

    br_i_inv_sparse = 1 - np.sum(br_i**(p + 1))
    dist_i_inv_sparse = 1 - np.sum(dist[i]**(p + 1))
    entr_br_i = s_i / (p + 1) * br_i_inv_sparse
    entr_dist_i = s_i / (p + 1) * dist_i_inv_sparse

    reg_exp.append(y[i].dot(br_i - dist[i]) + entr_br_i - entr_dist_i)

    entr_br_vec_i = br_i_inv_sparse * br_i**(1 - p)
    entr_dist_vec_i = dist_i_inv_sparse * dist[i]**(1 - p)
    other_player_fx_i = (br_i - dist[i]) + 1 / (p + 1) * (
        entr_br_vec_i - entr_dist_vec_i)
    other_player_fx.append(other_player_fx_i)

  # then construct exploitability gradient
  grad_dist = []
  for i in range(num_players):

    grad_dist_i = -policy_gradient[i]
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_j_ij = payoff_matrices[(i, j)][1]
      else:
        hess_j_ij = payoff_matrices[(j, i)][0].T

      grad_dist_i += hess_j_ij.dot(other_player_fx[j])

    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)

    grad_dist.append(grad_dist_i)

  return (grad_dist, grad_y), np.mean(unreg_exp), np.mean(reg_exp)


def gradients(dist, y, regret, payoff_matrices, num_players, p=1):
  """Computes exploitablity gradient and aux variable gradients.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    y: list 1-d np.arrays (same shape as dist), current est. of payoff gradient
    regret: list of 1-d np.arrays (same shape as dist), exploitability regrets
    payoff_matrices: dictionary with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
    p: float in [0, 1], Tsallis entropy-regularization --> 0 as p --> 0
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
  del regret

  # first compute policy gradients and player effects (fx)
  policy_gradient = []
  other_player_fx = []
  grad_y = []
  unreg_exp = []
  reg_exp = []
  for i in range(num_players):

    nabla_i = np.zeros_like(dist[i])
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij = payoff_matrices[(i, j)][0]
      else:
        hess_i_ij = payoff_matrices[(j, i)][1].T

      nabla_ij = hess_i_ij.dot(dist[j])
      nabla_i += nabla_ij / float(num_players - 1)

    grad_y.append(y[i] - nabla_i)
    y[i] = nabla_i  # TODO(imgemp): overwriting temporarily to test something

    if p > 0:
      power = 1. / float(p)
      s_i = np.linalg.norm(y[i], ord=power)
      if s_i == 0:
        br_i = misc.uniform_dist(y[i])
      else:
        br_i = (y[i] / s_i)**power
    else:
      power = np.inf
      s_i = np.linalg.norm(y[i], ord=power)
      br_i = np.zeros_like(dist[i])
      maxima_i = (y[i] == s_i)
      br_i[maxima_i] = 1. / maxima_i.sum()

    policy_gradient_i = nabla_i - s_i * dist[i]**p
    policy_gradient.append(policy_gradient_i)

    unreg_exp.append(np.max(y[i]) - y[i].dot(dist[i]))

    br_i_inv_sparse = 1 - np.sum(br_i**(p + 1))
    dist_i_inv_sparse = 1 - np.sum(dist[i]**(p + 1))
    entr_br_i = s_i / (p + 1) * br_i_inv_sparse
    entr_dist_i = s_i / (p + 1) * dist_i_inv_sparse

    reg_exp.append(y[i].dot(br_i - dist[i]) + entr_br_i - entr_dist_i)

    entr_br_vec_i = br_i_inv_sparse * br_i**(1 - p)
    entr_dist_vec_i = dist_i_inv_sparse * dist[i]**(1 - p)
    other_player_fx_i = (br_i - dist[i]) + 1 / (p + 1) * (
        entr_br_vec_i - entr_dist_vec_i)
    other_player_fx.append(other_player_fx_i)

  # then construct exploitability gradient
  grad_dist = []
  regret_delta = []
  for i in range(num_players):

    grad_dist_i = -policy_gradient[i]
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_j_ij = payoff_matrices[(i, j)][1]
      else:
        hess_j_ij = payoff_matrices[(j, i)][0].T

      grad_dist_i += hess_j_ij.dot(other_player_fx[j])

    regret_delta_i = -(grad_dist_i - grad_dist_i.dot(dist[i]))
    # regret_delta_i = y[i] - y[i].dot(dist[i])

    grad_dist.append(grad_dist_i)
    regret_delta.append(regret_delta_i)

  return (grad_dist, grad_y, regret_delta), np.mean(unreg_exp), np.mean(reg_exp)


def gradients(dist, payoff_matrices, num_players, proj_grad=True):
  """Computes exploitablity gradient.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    payoff_matrices: dictionary with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist) as tuple
    unregularized exploitability (stochastic estimate)
    unregularized exploitability (stochastic estimate) *duplicate
  """
  # first compute best responses and payoff gradients
  nabla = []
  br = []
  unreg_exp = []
  for i in range(num_players):

    nabla_i = np.zeros_like(dist[i])
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij = payoff_matrices[(i, j)][0]
      else:
        hess_i_ij = payoff_matrices[(j, i)][1].T

      nabla_ij = hess_i_ij.dot(dist[j])
      nabla_i += nabla_ij / float(num_players - 1)

    nabla.append(nabla_i)

    power = np.inf
    s_i = np.linalg.norm(nabla_i, ord=power)
    br_i = np.zeros_like(nabla_i)
    maxima_i = (nabla_i == s_i)
    br_i[maxima_i] = 1. / maxima_i.sum()
    br.append(br_i)

    unreg_exp.append(np.max(nabla_i) - nabla_i.dot(dist[i]))

  # then construct exploitability gradient
  grad_dist = []
  for i in range(num_players):

    grad_dist_i = -nabla[i]
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_j_ij = payoff_matrices[(i, j)][1]
      else:
        hess_j_ij = payoff_matrices[(j, i)][0].T

      grad_dist_i += hess_j_ij.dot(br[j] - dist[j])

    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)

    grad_dist.append(grad_dist_i)

  return (grad_dist,), np.mean(unreg_exp), np.mean(unreg_exp)


def gradients(dist, payoff_matrices, num_players, proj_grad=True):
  """Computes exploitablity gradient.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    payoff_matrices: dictionary with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of payoff w.r.t. (dist) as tuple
    unregularized exploitability (stochastic estimate)
    unregularized exploitability (stochastic estimate) *duplicate
  """
  # first compute best responses and payoff gradients
  grad_dist = []
  unreg_exp = []
  for i in range(num_players):

    nabla_i = np.zeros_like(dist[i])
    # TODO(imgemp): decide if averaging over nablas provides best comparison
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij = payoff_matrices[(i, j)][0]
      else:
        hess_i_ij = payoff_matrices[(j, i)][1].T

      nabla_ij = hess_i_ij.dot(dist[j])
      nabla_i += nabla_ij / float(num_players - 1)

    grad_dist_i = -nabla_i
    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)
    grad_dist.append(nabla_i)

    unreg_exp.append(np.max(nabla_i) - nabla_i.dot(dist[i]))

  return (grad_dist,), np.mean(unreg_exp), np.mean(unreg_exp)


def gradients(dist, y, payoff_matrices, num_players, temperature=0.,
              proj_grad=True):
  """Computes exploitablity gradient and aux variable gradients.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    y: list 1-d np.arrays (same shape as dist), current est. of payoff gradient
    payoff_matrices: dictionary with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
    temperature: non-negative float, default 0.
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    shannon regularized exploitability (stochastic estimate)
  """
  # first compute policy gradients and player effects (fx)
  policy_gradient = []
  other_player_fx = []
  grad_y = []
  unreg_exp = []
  reg_exp = []
  for i in range(num_players):

    nabla_i = np.zeros_like(dist[i])
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij = payoff_matrices[(i, j)][0]
      else:
        hess_i_ij = payoff_matrices[(j, i)][1].T

      nabla_ij = hess_i_ij.dot(dist[j])
      nabla_i += nabla_ij / float(num_players - 1)

    grad_y.append(y[i] - nabla_i)

    if temperature > 0:
      br_i = special.softmax(y[i] / temperature)
      br_i_policy_gradient = nabla_i - temperature * (np.log(br_i) + 1)
    else:
      power = np.inf
      s_i = np.linalg.norm(y[i], ord=power)
      br_i = np.zeros_like(dist[i])
      maxima_i = (y[i] == s_i)
      br_i[maxima_i] = 1. / maxima_i.sum()
      br_i_policy_gradient = np.zeros_like(br_i)

    policy_gradient_i = nabla_i
    if temperature > 0:
      policy_gradient_i -= temperature * (np.log(dist[i]) + 1)
    policy_gradient.append(policy_gradient_i)

    unreg_exp.append(np.max(y[i]) - y[i].dot(dist[i]))

    entr_br_i = temperature * special.entr(br_i).sum()
    entr_dist_i = temperature * special.entr(dist[i]).sum()

    reg_exp.append(y[i].dot(br_i - dist[i]) + entr_br_i - entr_dist_i)

    other_player_fx_i = (br_i - dist[i])
    if temperature > 0:
      # much faster to avoid constructing br_i_mat and then computing
      # br_i_mat.dot(br_policy_gradient) -- instead, expand out and only compute
      # inner products
      temp = (br_i_policy_gradient - br_i.dot(br_i_policy_gradient))
      other_player_fx_i += br_i / temperature * temp
    other_player_fx.append(other_player_fx_i)

  # then construct exploitability gradient
  grad_dist = []
  for i in range(num_players):

    grad_dist_i = -policy_gradient[i]
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_j_ij = payoff_matrices[(i, j)][1]
      else:
        hess_j_ij = payoff_matrices[(j, i)][0].T

      grad_dist_i += hess_j_ij.dot(other_player_fx[j])

    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)

    grad_dist.append(grad_dist_i)

  return (grad_dist, grad_y), np.mean(unreg_exp), np.mean(reg_exp)


def gradients(dist, regret, payoff_matrices, num_players):
  """Computes regret delta to be added to regret in update.

  Args:
    dist: list of 1-d np.arrays, current estimate of nash distribution
    regret: list of 1-d np.arrays (same as dist), current estimate of regrets
    payoff_matrices: dictionary with keys as tuples of agents (i, j) and
        values of (2 x A x A) np.arrays, payoffs for each joint action. keys
        are sorted and arrays should be indexed in the same order
    num_players: int, number of players, in case payoff_matrices is abbreviated
  Returns:
    deltas w.r.t. (dist, regret) as tuple
    unregularized exploitability (stochastic estimate)
    solver exploitability (stochastic estimate) - NaN
  """
  del regret

  # first compute best responses and payoff gradients
  grad_dist = []
  grad_regret = []
  unreg_exp = []
  for i in range(num_players):

    nabla_i = np.zeros_like(dist[i])
    # TODO(imgemp): decide if averaging over nablas provides best comparison
    for j in range(num_players):
      if j == i:
        continue
      if i < j:
        hess_i_ij = payoff_matrices[(i, j)][0]
      else:
        hess_i_ij = payoff_matrices[(j, i)][1].T

      nabla_ij = hess_i_ij.dot(dist[j])
      nabla_i += nabla_ij / float(num_players - 1)

    grad_dist_i = np.nan * np.ones_like(nabla_i)
    grad_dist.append(grad_dist_i)

    utility_i = nabla_i.dot(dist[i])
    grad_regret_i = nabla_i - utility_i
    grad_regret.append(grad_regret_i)

    unreg_exp.append(np.max(nabla_i) - nabla_i.dot(dist[i]))

  return (grad_dist, grad_regret), np.mean(unreg_exp), np.nan


def gradients(dist, payoff_matrices, num_players, temperature=0.,
              proj_grad=True):
  """Computes exploitablity gradient.

  Assumption: eta_k = 1 for all k

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


def gradients(dist, payoff_matrices, num_players, temperature=0.,
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


def gradients(dist, y, payoff_matrices, num_players, p=1, proj_grad=True):
  """Computes exploitablity gradient and aux variable gradients.

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
    num_players: int, number of players, in case payoff_matrices is abbreviated
    p: float in [0, 1], Tsallis entropy-regularization --> 0 as p --> 0
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
  nabla = payoff_matrices[0].dot(dist)
  if p > 0:
    power = 1. / float(p)
    s = np.linalg.norm(y, ord=power)
    if s == 0:
      br = misc.uniform_dist(y)
    else:
      br = (y / s)**power
  else:
    power = np.inf
    s = np.linalg.norm(y, ord=power)
    br = np.zeros_like(dist)
    maxima = (y == s)
    br[maxima] = 1. / maxima.sum()

  unreg_exp = np.max(y) - y.dot(dist)
  br_inv_sparse = 1 - np.sum(br**(p + 1))
  dist_inv_sparse = 1 - np.sum(dist**(p + 1))
  entr_br = s / (p + 1) * br_inv_sparse
  entr_dist = s / (p + 1) * dist_inv_sparse
  reg_exp = y.dot(br - dist) + entr_br - entr_dist

  entr_br_vec = br_inv_sparse * br**(1 - p)
  entr_dist_vec = dist_inv_sparse * dist**(1 - p)

  policy_gradient = nabla - s * dist**p
  other_player_fx = (br - dist) + 1 / (p + 1) * (entr_br_vec - entr_dist_vec)

  other_player_fx_translated = payoff_matrices[1].dot(other_player_fx)
  grad_dist = -policy_gradient + (num_players - 1) * other_player_fx_translated
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)
  grad_y = y - nabla

  return (grad_dist, grad_y), unreg_exp, reg_exp


def gradients(dist, payoff_matrices, num_players, proj_grad=True):
  """Computes exploitablity gradient.

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
    num_players: int, number of players, in case payoff_matrices is abbreviated
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist) as tuple
    unregularized exploitability (stochastic estimate)
    unregularized exploitability (stochastic estimate) *duplicate
  """
  nabla = payoff_matrices[0].dot(dist)

  power = np.inf
  s = np.linalg.norm(nabla, ord=power)
  br = np.zeros_like(dist)
  maxima = (nabla == s)
  br[maxima] = 1. / maxima.sum()

  unreg_exp = np.max(nabla) - nabla.dot(dist)

  grad_dist = -(nabla) + (num_players - 1) * payoff_matrices[1].dot(br - dist)
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)

  return (grad_dist,), unreg_exp, unreg_exp


def gradients(dist, payoff_matrices, proj_grad=True):
  """Computes exploitablity gradient.

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of payoff w.r.t. (dist) as tuple
    unregularized exploitability (stochastic estimate)
    unregularized exploitability (stochastic estimate) *duplicate
  """
  nabla = payoff_matrices[0].dot(dist)

  unreg_exp = np.max(nabla) - nabla.dot(dist)

  grad_dist = -nabla
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)

  return (grad_dist,), unreg_exp, unreg_exp


def gradients(dist, y, payoff_matrices, num_players, temperature=0.,
              proj_grad=True):
  """Computes exploitablity gradient and aux variable gradients.

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
    num_players: int, number of players, in case payoff_matrices is abbreviated
    temperature: non-negative float, default 0.
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
  nabla = payoff_matrices[0].dot(dist)
  if temperature > 0:
    br = special.softmax(y / temperature)
    br_policy_gradient = nabla - temperature * (np.log(br) + 1)
  else:
    power = np.inf
    s = np.linalg.norm(y, ord=power)
    br = np.zeros_like(dist)
    maxima = (y == s)
    br[maxima] = 1. / maxima.sum()
    br_policy_gradient = np.zeros_like(br)

  unreg_exp = np.max(y) - y.dot(dist)
  entr_br = temperature * special.entr(br).sum()
  entr_dist = temperature * special.entr(dist).sum()
  reg_exp = y.dot(br - dist) + entr_br - entr_dist

  policy_gradient = nabla
  if temperature > 0:
    policy_gradient -= temperature * (np.log(dist) + 1)
  other_player_fx = (br - dist)
  if temperature > 0:
    # much faster to avoid constructing br_mat and then computing
    # br_mat.dot(br_policy_gradient) -- instead, expand out and only compute
    # inner products
    temp = (br_policy_gradient - br.dot(br_policy_gradient))
    other_player_fx += br / temperature * temp

  other_player_fx_translated = payoff_matrices[1].dot(other_player_fx)
  grad_dist = -policy_gradient + (num_players - 1) * other_player_fx_translated
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)
  grad_y = y - nabla

  return (grad_dist, grad_y), unreg_exp, reg_exp


def gradients(dist, regret, payoff_matrices):
  """Computes regret delta to be added to regret in update.

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    regret: 1-d np.array (same shape as dist), current estimate of regrets
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
  Returns:
    deltas w.r.t. (dist, regret) as tuple
    unregularized exploitability (stochastic estimate)
    solver exploitability (stochastic estimate) - NaN
  """
  del regret

  nabla = payoff_matrices[0].dot(dist)
  utility = nabla.dot(dist)

  grad_dist = np.nan * np.ones_like(dist)
  grad_regret = nabla - utility

  unreg_exp = np.max(nabla) - nabla.dot(dist)

  return (grad_dist, grad_regret), unreg_exp, np.nan


def gradients(dist, payoff_matrices, num_players, temperature=0.,
              proj_grad=True):
  """Computes exploitablity gradient.

  Assumption: eta_k = 1 for all k

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

