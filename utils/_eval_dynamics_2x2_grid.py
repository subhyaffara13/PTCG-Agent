
def _eval_dynamics_2x2_grid(dynamics, num_points):
  """Evaluates dynamics on a 2-D mesh-grid.

  Args:
    dynamics: Population dynamics of type `dynamics.MultiPopulationDynamics`.
    num_points: Number of points along each dimension of the grid.

  Returns:
    Mesh-grid (x, y) and corresponding derivatives of the first action for
      player 1 and 2 (u, v).
  """
  assert dynamics.payoff_tensor.shape == (2, 2, 2)

  x = np.linspace(0., 1., num_points + 2)[1:-1]
  x, y = np.meshgrid(x, x)
  u = np.empty(x.shape)
  v = np.empty(x.shape)

  for i in range(num_points):
    for j in range(num_points):
      row_state = np.array([x[i, j], 1. - x[i, j]])
      col_state = np.array([y[i, j], 1. - y[i, j]])
      state = np.concatenate((row_state, col_state))
      dstate = dynamics(state)
      u[i][j] = dstate[0]
      v[i][j] = dstate[2]
  return x, y, u, v

