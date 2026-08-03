import random

def cheap_gradients_vr(random, dist, y, payoff_matrices, num_players, pm_vr,
                       p=1, proj_grad=True, version=0):
  """Computes exploitablity gradient and aux variable gradients with samples.

  This implementation takes payoff_matrices as input so technically uses O(d^2)
  compute but only a single column of payoff_matrices is used to perform the
  update so can be re-implemented in O(d) if needed.

  Args:
    random: random number generator, np.random.RandomState(seed)
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
    num_players: int, number of players, in case payoff_matrices is abbreviated
    pm_vr: approximate payoff_matrix for variance reduction
    p: float in [0, 1], Tsallis entropy-regularization --> 0 as p --> 0
    proj_grad: bool, if True, projects dist gradient onto simplex
    version: int, default 0, two options for variance reduction
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
  if pm_vr is None:
    raise ValueError("pm_vr must be np.array of shape (num_strats, num_strats)")
  if (not isinstance(version, int)) or (version < 0) or (version > 1):
    raise ValueError("version must be non-negative int < 2")

  action_1 = random.choice(dist.size, p=dist)
  nabla = payoff_matrices[0][:, action_1]
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

  if version == 0:
    other_player_fx_translated = pm_vr.dot(other_player_fx)
    action_u = random.choice(dist.size)  # uniform, ~importance sampling
    other_player_fx = other_player_fx[action_u]
    pm_mod = dist.size * (payoff_matrices[1, :, action_u] - pm_vr[:, action_u])
    other_player_fx_translated += pm_mod * other_player_fx
  elif version == 1:
    other_player_fx_translated = np.sum(pm_vr, axis=1)
    action_u = random.choice(dist.size)  # uniform, ~importance sampling
    other_player_fx = other_player_fx[action_u]
    pm_mod = dist.size * payoff_matrices[1, :, action_u]
    r = dist.size * pm_vr[:, action_u]
    other_player_fx_translated += pm_mod * other_player_fx - r

  grad_dist = -policy_gradient + (num_players - 1) * other_player_fx_translated
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)
  grad_y = y - nabla

  if version == 0:
    pm_vr[:, action_u] = payoff_matrices[1, :, action_u]
  elif version == 1:
    pm_vr[:, action_u] = payoff_matrices[1, :, action_u] * other_player_fx

  return (grad_dist, grad_y), pm_vr, unreg_exp, reg_exp


def cheap_gradients_vr(random, dist, y, payoff_matrices, num_players, pm_vr,
                       temperature=0., proj_grad=True, version=0):
  """Computes exploitablity gradient and aux variable gradients with samples.

  This implementation takes payoff_matrices as input so technically uses O(d^2)
  compute but only a single column of payoff_matrices is used to perform the
  update so can be re-implemented in O(d) if needed.

  Args:
    random: random number generator, np.random.RandomState(seed)
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
    payoff_matrices: (>=2 x A x A) np.array, payoffs for each joint action
    num_players: int, number of players, in case payoff_matrices is abbreviated
    pm_vr: approximate payoff_matrix for variance reduction
    temperature: non-negative float, default 0.
    proj_grad: bool, if True, projects dist gradient onto simplex
    version: int, default 0, two options for variance reduction
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
  if pm_vr is None:
    raise ValueError("pm_vr must be np.array of shape (num_strats, num_strats)")
  if (not isinstance(version, int)) or (version < 0) or (version > 1):
    raise ValueError("version must be non-negative int < 2")

  action_1 = random.choice(dist.size, p=dist)
  nabla = payoff_matrices[0][:, action_1]
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

  if version == 0:
    other_player_fx_translated = pm_vr.dot(other_player_fx)
    action_u = random.choice(dist.size)  # uniform, ~importance sampling
    other_player_fx = other_player_fx[action_u]
    pm_mod = dist.size * (payoff_matrices[1, :, action_u] - pm_vr[:, action_u])
    other_player_fx_translated += pm_mod * other_player_fx
  elif version == 1:
    other_player_fx_translated = np.sum(pm_vr, axis=1)
    action_u = random.choice(dist.size)  # uniform, ~importance sampling
    other_player_fx = other_player_fx[action_u]
    pm_mod = dist.size * payoff_matrices[1, :, action_u]
    r = dist.size * pm_vr[:, action_u]
    other_player_fx_translated += pm_mod * other_player_fx - r

  grad_dist = -policy_gradient + (num_players - 1) * other_player_fx_translated
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)
  grad_y = y - nabla

  if version == 0:
    pm_vr[:, action_u] = payoff_matrices[1, :, action_u]
  elif version == 1:
    pm_vr[:, action_u] = payoff_matrices[1, :, action_u] * other_player_fx

  return (grad_dist, grad_y), pm_vr, unreg_exp, reg_exp

