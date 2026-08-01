
def rmsprop_momentum(step_size, gamma=0.9, eps=1e-8, momentum=0.9):
  """Construct optimizer triple for RMSProp with momentum.

  This optimizer is separate from the rmsprop optimizer because it needs to
  keep track of additional parameters.

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to a positive scalar.
    gamma: Decay parameter.
    eps: Epsilon parameter.
    momentum: Momentum parameter.

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)
  def init(x0):
    avg_sq_grad = jnp.zeros_like(x0)
    mom = jnp.zeros_like(x0)
    return x0, avg_sq_grad, mom
  def update(i, g, state):
    x, avg_sq_grad, mom = state
    avg_sq_grad = avg_sq_grad * gamma + jnp.square(g) * (1. - gamma)
    mom = momentum * mom + step_size(i) * g / jnp.sqrt(avg_sq_grad + eps)
    x = x - mom
    return x, avg_sq_grad, mom
  def get_params(state):
    x, _, _ = state
    return x
  return init, update, get_params

