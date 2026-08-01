
def _get_problem(
    name: str,
) -> dict[str, Any]:
  """Get test function in given numpy (xnp) framework."""

  def rosenbrock(x, xnp):
    return xnp.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1.0 - x[:-1]) ** 2)

  def himmelblau(p):
    x, y = p
    return (x**2 + y - 11.0) ** 2 + (x + y**2 - 7.0) ** 2

  def matyas(p):
    x, y = p
    return 0.26 * (x**2 + y**2) - 0.48 * x * y

  def eggholder(p, xnp):
    x, y = p
    return -(y + 47) * xnp.sin(
        xnp.sqrt(xnp.abs(x / 2.0 + y + 47.0))
    ) - x * xnp.sin(xnp.sqrt(xnp.abs(x - (y + 47.0))))

  def zakharov(x, xnp):
    ii = xnp.arange(1, len(x) + 1, step=1, dtype=x.dtype)
    sum1 = (x**2).sum()
    sum2 = (0.5 * ii * x).sum()
    answer = sum1 + sum2**2 + sum2**4
    return answer

  problems = {
      'rosenbrock': {
          'fun': lambda x: rosenbrock(x, jnp),
          'numpy_fun': lambda x: rosenbrock(x, np),
          'init': np.zeros(2),
          'minimum': 0.0,
          'minimizer': np.ones(2),
      },
      'himmelblau': {
          'fun': himmelblau,
          'numpy_fun': himmelblau,
          'init': np.ones(2),
          'minimum': 0.0,
          # himmelblau has actually multiple minimizers, we simply consider one.
          'minimizer': np.array([3.0, 2.0]),
      },
      'matyas': {
          'fun': matyas,
          'numpy_fun': matyas,
          'init': np.ones(2) * 6.0,
          'minimum': 0.0,
          'minimizer': np.zeros(2),
      },
      'eggholder': {
          'fun': lambda x: eggholder(x, jnp),
          'numpy_fun': lambda x: eggholder(x, np),
          'init': np.ones(2) * 6.0,
          'minimum': -959.6407,
          'minimizer': np.array([512.0, 404.22319]),
      },
      'zakharov': {
          'fun': lambda x: zakharov(x, jnp),
          'numpy_fun': lambda x: zakharov(x, np),
          'init': np.array([600.0, 700.0, 200.0, 100.0, 90.0, 1e3]),
          'minimum': 0.0,
          'minimizer': np.zeros(6),
      },
  }
  return problems[name]

