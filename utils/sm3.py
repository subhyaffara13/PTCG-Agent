
def sm3(
    learning_rate: jax.typing.ArrayLike, momentum: jax.typing.ArrayLike = 0.9
) -> base.GradientTransformationExtraArgs:
  r"""The SM3 optimizer.

  SM3 (Square-root of Minima of Sums of Maxima of Squared-gradients Method) is a
  memory-efficient adaptive optimizer designed to decrease memory overhead when
  training very large models, such as the Transformer for machine translation,
  BERT for language modeling, and AmoebaNet-D for image classification. SM3: 1)
  applies to tensors of arbitrary dimensions and any predefined cover of the
  parameters; 2) adapts the learning rates in an adaptive and data-driven manner
  (like Adagrad and unlike Adafactor); and 3) comes with rigorous convergence
  guarantees in stochastic convex optimization settings.

  The init function of this optimizer initializes an internal state
  :math:`S_0 := \{\mu_0, w_1\} = \{0, 0\}`, representing initial estimates for
  the cumulative squared gradients and the weights. These values are stored as
  pytrees containing all zeros, with the same shape as the model updates. At
  step :math:`t`, the update function of this optimizer takes as arguments
  the incoming gradients :math:`g_t` and optimizer state :math:`S_t` and
  computes updates :math:`u_t` and new state :math:`S_{t+1}`. Thus, for
  :math:`t > 0`, we have:

  SM3-I Algorithm

  .. math::

      \begin{array}{l}
      \text{parameters: learning rate } \eta \\
      \text{initialize } w_1 = 0; \forall r \in [k]: \mu_0(r) = 0 \\
      \text{for } t = 1, \ldots, T \text{ do} \\
      \quad \text{receive gradient } g_t = \nabla \ell_t(w_t) \\
      \quad \text{for } r = 1, \ldots, k \text{ do} \\
      \quad \quad \mu_t(r) \leftarrow \mu_{t-1}(r) +
      \max_{j \in S_r} g_t^2(j) \\
      \quad \text{for } i = 1, \ldots, d \text{ do} \\
      \quad \quad \nu_t(i) \leftarrow \min_{r:S_r \ni i} \mu_t(r) \\
      \quad \quad w_{t+1}(i) \leftarrow w_t(i) -
      \eta \frac{g_t(i)}{\sqrt{\nu_t(i)}} \\
      \quad \quad \text{with the convention that } 0/0 = 0
      \end{array}

  SM3-II Algorithm

  The SM3-II optimizer initializes with parameters like the learning rate
  :math:\eta and weight :math:w_1. It updates weights iteratively using
  gradients :math:g_t, adjusting each component with minimum accumulated
  values :math:\nu'_t(i) and maintaining cumulative maximums :math:\mu'_t(r)
  for subsets :math:S_r. SM3-II starts with an initial state
  :math:S_0 := (m_0, s_0) set to zero, storing estimates for first and second
  moments as pytrees matching model updates' shape

  .. math::

      \begin{array}{l}
      \text{parameters: learning rate } \eta \\
      \text{initialize } w_1 = 0; \forall r \in [k]: \mu'_0(r) = 0 \\
      \text{for } t = 1, \ldots, T \text{ do} \\
      \quad \text{receive gradient } g_t = \nabla \ell_t(w_t) \\
      \quad \text{initialize } \mu'_t(r) = 0 \text{ for all } r \in [k] \\
      \quad \text{for } i = 1, \ldots, d \text{ do} \\
      \quad \quad \nu'_t(i) \leftarrow \min_{r:S_r \ni i}
      \mu'_{t-1}(r) + g_t^2(i) \\
      \quad \quad w_{t+1}(i) \leftarrow w_t(i) -
      \eta \frac{g_t(i)}{\sqrt{\nu'_t(i)}} \\
      \quad \quad \text{with the convention that } 0/0 = 0 \\
      \quad \text{for all } r : S_r \ni i \text{ do} \\
      \quad \quad \mu'_t(r) \leftarrow \max\{\mu'_t(r), \nu'_t(i)\}
      \end{array}

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    momentum: Decay rate used by the momentum term (when it is not set to
      `None`, then momentum is not used at all).

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.sm3(learning_rate=0.003)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.40E+01
    Objective function: 1.40E+01
    Objective function: 1.40E+01
    Objective function: 1.40E+01
    Objective function: 1.40E+01

  References:
    Anil et al, `Memory-Efficient Adaptive Optimization
    <https://arxiv.org/abs/1901.11150>`_, 2019
  """
  return combine.chain(
      transform.scale_by_sm3(momentum),
      transform.scale(-learning_rate),
  )


def sm3(step_size, momentum=0.9):
  """Construct optimizer triple for SM3.

  Memory-Efficient Adaptive Optimization for Large-Scale Learning.
  https://arxiv.org/abs/1901.11150

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to a positive scalar.
    momentum: optional, a positive scalar value for momentum

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)

  def splice(seq, i, x):
    lst = list(seq)
    lst[i:i+1] = x
    return lst

  def broadcast_into(ndim, x, axis):
    idx = splice([None] * ndim, axis, [slice(None)])
    return x[tuple(idx)]

  def init(x0):
    x_shape = x0.shape
    x0 = jnp.atleast_1d(x0)
    vs = [jnp.zeros(sz, dtype=x0.dtype) for sz in x0.shape]
    return x0, jnp.zeros_like(x0), vs, x_shape

  def update(i, g, state):
    x, m, vs, x_shape = state
    vs = [broadcast_into(g.ndim, v, i) for i, v in enumerate(vs)]
    accum = functools.reduce(jnp.minimum, vs) + jnp.square(g)
    accum_inv_sqrt = jnp.where(accum > 0, 1. / jnp.sqrt(accum), 0)
    m = (1. - momentum) * (g * accum_inv_sqrt) + momentum * m
    x = x - step_size(i) * m
    vs = [accum.max(splice(range(x.ndim), j, [])) for j in range(x.ndim)]
    return x, m, vs, x_shape

  def get_params(state):
    x, _, _, x_shape = state
    return x.reshape(x_shape)

  return init, update, get_params

