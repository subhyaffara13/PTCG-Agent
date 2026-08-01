
def _max_entropy_symmetric_nash_avt(p_mat, num_agents, num_tasks, eps=1e-9):
  """Solves for the maxent symmetric nash for symmetric 2P zero-sum games.

    This covers the agent-vs-task cases.

    Using convex programming:
      min x^Tlog(x) + y^Tlog(y)
      s.t.
      x >= 0
      1^T * x = 1
      y >= 0
      1^T * y = 1
      forall s, such that s has exactly one unit mass on an agent strategy
      and one unit mass on a task strategy,
      s^T*p_mat*z <= 0, where z = [x, y], since game-value is 0.

  Args:
    p_mat: an N*N anti-symmetric payoff matrix for the row player
    num_agents: number of agents
    num_tasks: number of tasks
    eps: minimum probability threshold

  Returns:
    (x*, y*): a maxent symmetric nash
  """
  assert np.array_equal(p_mat, -p_mat.T) and eps >= 0 and eps <= 0.5
  n = len(p_mat)
  assert n == num_agents + num_tasks
  x = cp.Variable(shape=num_agents)
  y = cp.Variable(shape=num_tasks)
  z = cp.hstack([x, y])
  obj = cp.Maximize(cp.sum(cp.entr(z)))
  constraints = [
      x >= eps * np.ones(num_agents),
      cp.sum(x) == 1,
      y >= eps * np.ones(num_tasks),
      cp.sum(y) == 1,
  ]

  dev_payoffs = p_mat @ z
  for a_idx in range(num_agents):
    for t_idx in range(num_tasks):
      pure_strategy = np.zeros(n)
      pure_strategy[a_idx] = 1
      pure_strategy[num_agents + t_idx] = 1
      pure_strategy = pure_strategy.reshape((1, -1))
      constraints.append(pure_strategy @ dev_payoffs <= 0)

  prob = cp.Problem(obj, constraints)
  prob.solve()
  return x.value.reshape((-1, 1)), y.value.reshape((-1, 1))

