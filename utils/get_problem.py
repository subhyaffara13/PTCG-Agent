
def get_problem(name: str):
  """Objectives to test linesearches on."""

  def polynomial(x):
    return -x - x**3 + x**4

  def exponential(x):
    return jnp.exp(-4 * x) + x**2

  def sinusoidal(x):
    return -jnp.sin(10 * x)

  def rosenbrock(x):
    return jnp.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1.0 - x[:-1]) ** 2)

  def himmelblau(x):
    return (x[0] ** 2 + x[1] - 11.0) ** 2 + (x[0] + x[1] ** 2 - 7.0) ** 2

  def matyas(x):
    return 0.26 * (x[0] ** 2 + x[1] ** 2) - 0.48 * x[0] * x[1]

  def eggholder(x):
    return -(x[1] + 47) * jnp.sin(
        jnp.sqrt(jnp.abs(x[0] / 2.0 + x[1] + 47.0))
    ) - x[0] * jnp.sin(jnp.sqrt(jnp.abs(x[0] - (x[1] + 47.0))))

  def zakharov(x):
    ii = jnp.arange(1, len(x) + 1, step=1, dtype=x.dtype)
    sum1 = (x**2).sum()
    sum2 = (0.5 * ii * x).sum()
    return sum1 + sum2**2 + sum2**4

  problems = {
      'polynomial': {'fn': polynomial, 'input_shape': ()},
      'exponential': {'fn': exponential, 'input_shape': ()},
      'sinusoidal': {'fn': sinusoidal, 'input_shape': ()},
      'rosenbrock': {'fn': rosenbrock, 'input_shape': (16,)},
      'himmelblau': {'fn': himmelblau, 'input_shape': (2,)},
      'matyas': {'fn': matyas, 'input_shape': (2,)},
      'eggholder': {'fn': eggholder, 'input_shape': (2,)},
      'zakharov': {'fn': zakharov, 'input_shape': (6,)},
  }
  return problems[name]

