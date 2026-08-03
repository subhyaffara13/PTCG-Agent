from typing import Any, Callable, Optional, Union

def adan(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.98,
    b2: jax.typing.ArrayLike = 0.92,
    b3: jax.typing.ArrayLike = 0.99,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 1e-8,
    weight_decay: base.ScalarOrSchedule = 0.0,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
) -> base.GradientTransformationExtraArgs:
  r"""The ADAptive Nesterov momentum algorithm (Adan).

  Adan first reformulates the vanilla Nesterov acceleration to develop a new
  Nesterov momentum estimation (NME) method, which avoids the extra overhead of
  computing gradient at the extrapolation point. Then Adan adopts NME to
  estimate the gradient's first- and second-order moments in adaptive gradient
  algorithms for convergence acceleration.

  The algorithm is as follows. First, we define the following parameters:

  - :math:`\eta > 0`: the step size.
  - :math:`\beta_1 \in [0, 1]`: the decay rate for the exponentially weighted
    average of gradients.
  - :math:`\beta_2 \in [0, 1]`: the decay rate for the exponentially weighted
    average of differences of gradients.
  - :math:`\beta_3 \in [0, 1]`: the decay rate for the exponentially weighted
    average of the squared term.
  - :math:`\varepsilon > 0`: a small constant for numerical stability.
  - :math:`\lambda > 0`: a weight decay.

  Second, we define the following variables:

  - :math:`\theta_t`: the parameters.
  - :math:`g_t`: the incoming stochastic gradient.
  - :math:`m_t`: the exponentially weighted average of gradients.
  - :math:`v_t`: the exponentially weighted average of differences of gradients.
  - :math:`n_t`: the exponentially weighted average of the squared term.
  - :math:`u_t`: the outgoing update vector.
  - :math:`S_t`: the saved state of the optimizer.

  Third, we initialize these variables as follows:

  - :math:`m_0 = g_0`
  - :math:`v_0 = 0`
  - :math:`v_1 = g_1 - g_0`
  - :math:`n_0 = g_0^2`

  Finally, on each iteration, we update the variables as follows:

  .. math::

    \begin{align*}
      m_t &\gets (1 - \beta_1) m_{t-1} + \beta_1 g_t \\
      v_t &\gets (1 - \beta_2) v_{t-1} + \beta_2 (g_t - g_{t-1}) \\
      n_t &\gets (1 - \beta_3) n_{t-1} + \beta_3 (g_t + (1 - \beta_2)
        (g_t - g_{t-1}))^2 \\
      \eta_t &\gets \eta / ({\sqrt{n_t + \bar{\varepsilon}} + \varepsilon}) \\
      u_t &\gets (\theta_t - \eta_t \circ (m_t + (1 - \beta_2) v_t))
        / (1 + \lambda \eta) \\
      S_t &\leftarrow (m_t, v_t, n_t).
    \end{align*}

  Args:
    learning_rate: this is a fixed global scaling factor.
    b1: Decay rate for the EWMA of gradients.
    b2: Decay rate for the EWMA of differences of gradients.
    b3: Decay rate for the EMWA of the algorithm's squared term.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the denominator inside the square-root to improve
      numerical stability when backpropagating gradients through the rescaling.
    weight_decay: Strength of the weight decay regularization.
    mask: A tree with same structure as (or a prefix of) the params PyTree,
      or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the weight decay to, and `False` for those you want to skip.

  Returns:
    the corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> f = lambda x: x @ x  # simple quadratic function
    >>> solver = optax.adan(learning_rate=1e-1)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.28E+01
    Objective function: 1.17E+01
    Objective function: 1.07E+01
    Objective function: 9.68E+00
    Objective function: 8.76E+00

  References:
    Xie et al, `Adan: Adaptive Nesterov Momentum Algorithm for Faster Optimizing
    Deep Models
    <https://arxiv.org/abs/2208.06677>`_, 2022
  """
  return combine.chain(
      transform.scale_by_adan(
          b1=b1,
          b2=b2,
          b3=b3,
          eps=eps,
          eps_root=eps_root,
      ),
      transform.add_decayed_weights(weight_decay, mask),
      transform.scale_by_learning_rate(learning_rate),
  )

