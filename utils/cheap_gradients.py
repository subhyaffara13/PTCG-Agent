
def cheap_gradients(random, dist, y, payoff_matrices, num_players, p=1,
                    proj_grad=True):
  """Computes exploitablity gradient and aux variable gradients with samples.

  This implementation takes payoff_matrices as input so technically uses O(d^2)
  compute but only a single column of payoff_matrices is used to perform the
  update so can be re-implemented in O(d) if needed.

  Args:
    random: random number generator, np.random.RandomState(seed)
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

    others = list(range(num_players))
    others.remove(i)
    j = np.random.choice(others)
    action_j = random.choice(dist[j].size, p=dist[j])
    if i < j:
      hess_i_ij = payoff_matrices[(i, j)][0]
    else:
      hess_i_ij = payoff_matrices[(j, i)][1].T
    nabla_i = hess_i_ij[:, action_j]

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

      action_u = random.choice(dist[j].size)  # uniform, ~importance sampling
      other_player_fx_j = dist[j].size * other_player_fx[j][action_u]
      grad_dist_i += hess_j_ij[:, action_u] * other_player_fx_j

    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)

    grad_dist.append(grad_dist_i)

  return (grad_dist, grad_y), np.mean(unreg_exp), np.mean(reg_exp)


def cheap_gradients(random, dist, y, payoff_matrices, num_players,
                    temperature=0., proj_grad=True):
  """Computes exploitablity gradient and aux variable gradients with samples.

  This implementation takes payoff_matrices as input so technically uses O(d^2)
  compute but only a single column of payoff_matrices is used to perform the
  update so can be re-implemented in O(d) if needed.

  Args:
    random: random number generator, np.random.RandomState(seed)
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

    others = list(range(num_players))
    others.remove(i)
    j = np.random.choice(others)
    action_j = random.choice(dist[j].size, p=dist[j])
    if i < j:
      hess_i_ij = payoff_matrices[(i, j)][0]
    else:
      hess_i_ij = payoff_matrices[(j, i)][1].T
    nabla_i = hess_i_ij[:, action_j]

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

      action_u = random.choice(dist[j].size)  # uniform, ~importance sampling
      other_player_fx_j = dist[j].size * other_player_fx[j][action_u]
      grad_dist_i += hess_j_ij[:, action_u] * other_player_fx_j

    if proj_grad:
      grad_dist_i = simplex.project_grad(grad_dist_i)

    grad_dist.append(grad_dist_i)

  return (grad_dist, grad_y), np.mean(unreg_exp), np.mean(reg_exp)


def cheap_gradients(random, dist, y, payoff_matrices, num_players, p=1,
                    proj_grad=True):
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
    p: float in [0, 1], Tsallis entropy-regularization --> 0 as p --> 0
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
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

  action_u = random.choice(dist.size)  # uniform, ~importance sampling
  other_player_fx = dist.size * other_player_fx[action_u]
  other_player_fx_translated = payoff_matrices[1, :, action_u] * other_player_fx
  grad_dist = -policy_gradient + (num_players - 1) * other_player_fx_translated
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)
  grad_y = y - nabla

  return (grad_dist, grad_y), unreg_exp, reg_exp


def cheap_gradients(random, dist, y, payoff_matrices, num_players,
                    temperature=0., proj_grad=True):
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
    temperature: non-negative float, default 0.
    proj_grad: bool, if True, projects dist gradient onto simplex
  Returns:
    gradient of exploitability w.r.t. (dist, y) as tuple
    unregularized exploitability (stochastic estimate)
    tsallis regularized exploitability (stochastic estimate)
  """
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

  action_u = random.choice(dist.size)  # uniform, ~importance sampling
  other_player_fx = dist.size * other_player_fx[action_u]
  other_player_fx_translated = payoff_matrices[1, :, action_u] * other_player_fx
  grad_dist = -policy_gradient + (num_players - 1) * other_player_fx_translated
  if proj_grad:
    grad_dist = simplex.project_grad(grad_dist)
  grad_y = y - nabla

  return (grad_dist, grad_y), unreg_exp, reg_exp

