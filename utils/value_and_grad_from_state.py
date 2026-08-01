
def value_and_grad_from_state(
    value_fn: Callable[..., jax.typing.ArrayLike],
) -> Callable[..., tuple[jax.typing.ArrayLike, base.Updates]]:
  r"""Alternative to :func:`jax.value_and_grad` fetches value, grad from state.

  Line-search methods such as :func:`optax.scale_by_backtracking_linesearch`
  require to compute the gradient and objective function at the candidate
  iterate. This objective value and gradient can be re-used in the next
  iteration to save some computations using this utility function.

  Args:
    value_fn: function returning a scalar (float or array of dimension 1),
      amenable to differentiation in jax using :func:`jax.value_and_grad`.

  Returns:
    A callable akin to :func:`jax.value_and_grad` that fetches value
    and grad from the state if present. If no value or grad are found or if
    multiple value and grads are found this function raises an error. If a value
    is found but is infinite or nan, the value and grad are computed using
    :func:`jax.value_and_grad`. If the gradient found in the state is None,
    raises an Error.


  Examples:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> def fn(x): return jnp.sum(x ** 2)
    >>> solver = optax.chain(
    ...     optax.sgd(learning_rate=1.),
    ...     optax.scale_by_backtracking_linesearch(
    ...         max_backtracking_steps=15, store_grad=True
    ...     )
    ... )
    >>> value_and_grad = optax.value_and_grad_from_state(fn)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: {:.2E}'.format(fn(params)))
    Objective function: 1.40E+01
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...   value, grad = value_and_grad(params, state=opt_state)
    ...   updates, opt_state = solver.update(
    ...       grad, opt_state, params, value=value, grad=grad, value_fn=fn
    ...   )
    ...   params = optax.apply_updates(params, updates)
    ...   print('Objective function: {:.2E}'.format(fn(params)))
    Objective function: 5.04E+00
    Objective function: 1.81E+00
    Objective function: 6.53E-01
    Objective function: 2.35E-01
    Objective function: 8.47E-02
  """

  def _value_and_grad(
      params: base.Params,
      *fn_args: Any,
      state: base.OptState,
      **fn_kwargs: dict[str, Any],
  ):
    value = optax.tree.get(state, "value")
    grad = optax.tree.get(state, "grad")
    if (value is None) or (grad is None):
      raise ValueError(
          "Value or gradient not found in the state. "
          "Make sure that these values are stored in the state by the "
          "optimizer."
      )
    value, grad = jax.lax.cond(
        (~jnp.isinf(value)) & (~jnp.isnan(value)),
        lambda *_: (value, grad),
        lambda p, a, kwa: jax.value_and_grad(value_fn)(p, *a, **kwa),
        params,
        fn_args,
        fn_kwargs,
    )
    return value, grad

  return _value_and_grad

