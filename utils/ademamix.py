
def ademamix(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    b3: base.ScalarOrSchedule = 0.9999,
    alpha: base.ScalarOrSchedule = 5.0,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    mu_dtype: Optional[Any] = None,
    weight_decay: jax.typing.ArrayLike = 0.0,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
) -> base.GradientTransformation:
  r"""AdEMAMix.

  AdEMAMix (Adaptive EMA Mixture) is AdamW with a mixture of two momentum
  terms to better take advantage of historical gradients.

  Both SGD with momentum (SGD+M) and Adam incorporate momentum using
  Exponential Moving Averages (EMAs) of past gradients

  Let :math:`\eta` represent the learning rate and :math:`\beta_1, \beta_2`,
  :math:`\beta_3, \alpha, \varepsilon, \bar{\varepsilon}`, represent the
  arguments ``b1``, ``b2``, ``b3``, ``alpha``, ``eps``  and ``eps_root``
  respectively. Let :math:`\lambda` be the weight decay and :math:`\theta_t`
  the parameter vector at time :math:`t`.

  The ``init`` function of this optimizer initializes an internal state
  :math:`S_0 := (m^{(1)}_0, m^{(2)}_0, \nu_0) = (0, 0, 0)`, representing initial
  estimates for the fast and slow EMAs of the first moment along with the second
  moment estimate. In practice, these values are stored as pytrees containing
  all zeros, with the same shape as the model updates.  At step :math:`t`,
  the ``update`` function of this optimizer takes as arguments the incoming
  gradients :math:`g^t`, the optimizer state :math:`S^t` and the parameters
  :math:`\theta^{(t)}`. It then computes updates :math:`\theta^{(t+1)}` and the
  new state :math:`S^{(t+1)}`. Thus, for :math:`t > 0`, we have,

  .. math::

    \begin{align*}
      m_1^{(t)} &\leftarrow \beta_1 \cdot m_1^{(t-1)} + (1-\beta_1)
      \cdot g^{(t)} \\
      m_2^{(t)} &\leftarrow \beta_3 \cdot m_2^{(t-1)} + (1-\beta_3) \cdot
      g^{(t)} \\
      \nu^{(t)} &\leftarrow \beta_2 \cdot \nu^{(t-1)} + (1-\beta_2) \cdot
      {g^{(t)}}^2 \\
      \hat{m_1}^{(t)} &\leftarrow m_1^{(t)} / {(1-\beta_1^{(t)})} \\
      \hat{\nu}^{(t)} &\leftarrow \nu^{(t)} / {(1-\beta_2^{(t)})} \\
      \theta^{(t)} &\leftarrow \theta^{(t-1)} - \eta \cdot \left(
      \frac{(\hat{m_1}^{(t)} + \alpha m_2^{(t)})}{\left(\sqrt{\hat{\nu}^{(t)}
      + \bar{\varepsilon}} + \varepsilon\right)} + \lambda \theta^{(t-1)}
      \right).\\
      S^{(t)} &\leftarrow (m_1^{(t)}, m_2^{(t)}, v^{(t)}).
    \end{align*}

  .. note::
    AdEMAMix consists in leveraging very old gradients. Therefore,
    the method is best suited to settings where the number of iterations is
    important. The paper reports on this effect in Appendix C.1.5, showing how
    smaller values of ``b3`` (e.g. ``b3 = 0.999``) can be better for low
    iterations scenarios. Moreover, retaining gradient information over many
    thousands of steps can pose a problem in domains requiring fast adaptation
    to a sudden distribution shift, or general cases in which the distribution
    is non-stationary.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(jnp.square(x))  # simple quadratic function
    >>> solver = optax.contrib.ademamix(learning_rate=0.01)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.39E+01
    Objective function: 1.38E+01
    Objective function: 1.36E+01
    Objective function: 1.35E+01
    Objective function: 1.34E+01

  References:
    Pagliardini et al, `The AdEMAMix Optimizer: Better, Faster, Older
    <https://arxiv.org/abs/2409.03137>`_, 2024

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Exponential decay rate to track the fast EMA.
    b2: Exponential decay rate to track the second moment of past gradients.
    b3: Exponential decay rate to track the slow EMA.
    alpha: Mixing coefficient in the linear combination fo the fast and
      slow EMAs.
    eps: A small constant applied to denominator outside of the square root
      (as in the Adam paper) to avoid dividing by zero when rescaling.
    eps_root: A small constant applied to denominator inside the square root (as
      in RMSProp), to avoid dividing by zero when rescaling. This is needed for
      instance when computing (meta-)gradients through Adam.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.
    weight_decay: Strength of the weight decay regularization. Note that this
      weight decay is multiplied with the learning rate. This is consistent
      with other frameworks such as PyTorch, but different from
      (Loshchilov et al, 2019) where the weight decay is only multiplied with
      the "schedule multiplier", but not the base learning rate.
    mask: A tree with same structure as (or a prefix of) the params PyTree,
      or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the weight decay to, and `False` for those you want to skip. Note
      that the Adam gradient transformations are applied to all parameters.

  Returns:
    The corresponding `GradientTransformation`.

  .. seealso::
    See the related functions :func:`optax.adam`, :func:`optax.nadamw`, as well
    as the example
    :doc:`../../_collections/examples/contrib/rosenbrock_ademamix` for a use
    case.
  """
  return combine.chain(
      scale_by_ademamix(
          b1=b1,
          b2=b2,
          b3=b3,
          alpha=alpha,
          eps=eps,
          eps_root=eps_root,
          mu_dtype=mu_dtype,
      ),
      transform.add_decayed_weights(weight_decay, mask),
      transform.scale_by_learning_rate(learning_rate),
  )

