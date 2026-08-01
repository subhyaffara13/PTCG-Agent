
def scale_by_backtracking_linesearch(
    max_backtracking_steps: jax.typing.ArrayLike,  # int
    slope_rtol: jax.typing.ArrayLike = 1e-4,
    decrease_factor: jax.typing.ArrayLike = 0.8,
    increase_factor: jax.typing.ArrayLike = 1.5,
    max_learning_rate: jax.typing.ArrayLike = 1.0,
    atol: jax.typing.ArrayLike = 0.0,
    rtol: jax.typing.ArrayLike = 0.0,
    store_grad: bool = False,
    verbose: bool = False,
) -> base.GradientTransformationExtraArgs:
  r"""Backtracking line-search ensuring sufficient decrease (Armijo criterion).

  Selects learning rate :math:`\eta` such that it verifies the sufficient
  decrease criterion

  .. math::
    f(w + \eta u) \leq (1+\delta)f(w) + \eta c \langle u, \nabla f(w) \rangle +
    \epsilon \,,

  where

    :math:`f` is the function to minimize,
    :math:`w` are the current parameters,
    :math:`\eta` is the learning rate to find,
    :math:`u` is the update direction,
    :math:`c` is a coefficient (``slope_rtol``) measuring the relative decrease
    of the function in terms of the slope (scalar product between the gradient
    and the updates),
    :math:`\delta` is a relative tolerance (``rtol``),
    :math:`\epsilon` is an absolute tolerance (``atol``).

  The algorithm starts with a given guess of a learning rate and decrease it
  by ``decrease_factor`` until the criterion above is met.

  Args:
    max_backtracking_steps: maximum number of iterations for the line-search.
    slope_rtol: relative tolerance w.r.t. to the slope. The sufficient decrease
      must be slope_rtol * lr * <grad, updates>, see formula above.
    decrease_factor: decreasing factor to reduce learning rate.
    increase_factor: increasing factor to increase learning rate guess. Setting
      it to 1. amounts to keep the current guess, setting it to ``math.inf``
      amounts to start with ``max_learning_rate`` at each round.
    max_learning_rate: maximum learning rate (learning rate guess clipped to
      this).
    atol: absolute tolerance at which the criterion needs to be satisfied.
    rtol: relative tolerance at which the criterion needs to be satisfied.
    store_grad: whether to compute and store the gradient at the end of the
      linesearch. Since the function is called to compute the value to accept
      the learning rate, we can also access the gradient along the way. By doing
      that, we can directly reuse the value and the gradient computed at the end
      of the linesearch for the next iteration using
      :func:`optax.value_and_grad_from_state`. See the example above.
    verbose: whether to print debugging information.

  Returns:
    A :class:`GradientTransformationExtraArgs`, where the ``update`` function
    takes the following additional keyword arguments:

    * ``value``: value of the function at the current params.
    * ``grad``: gradient of the function at the current params.
    * ``value_fn``: function returning the value of the function we seek to
      optimize.
    * ``**extra_args``: additional keyword arguments, if the function needs
      additional arguments such as input data, they should be put there (
      see example in this docstring).

  Examples:

    An example on using the backtracking line-search with SGD::

      >>> import optax
      >>> import jax
      >>> import jax.numpy as jnp
      >>> solver = optax.chain(
      ...    optax.sgd(learning_rate=1.),
      ...    optax.scale_by_backtracking_linesearch(max_backtracking_steps=15)
      ... )
      >>> # Function with additional inputs other than params
      >>> def fn(params, x, y): return optax.l2_loss(x.dot(params), y)
      >>> params = jnp.array([1., 2., 3.])
      >>> opt_state = solver.init(params)
      >>> x, y = jnp.array([3., 2., 1.]), jnp.array(0.)
      >>> xs, ys = jnp.tile(x, (5, 1)), jnp.tile(y, (5,))
      >>> opt_state = solver.init(params)
      >>> print('Objective function: {:.2E}'.format(fn(params, x, y)))
      Objective function: 5.00E+01
      >>> for x, y in zip(xs, ys):
      ...   value, grad = jax.value_and_grad(fn)(params, x, y)
      ...   updates, opt_state = solver.update(
      ...       grad,
      ...       opt_state,
      ...       params,
      ...       value=value,
      ...       grad=grad,
      ...       value_fn=fn,
      ...       x=x,
      ...       y=y
      ...   )
      ...   params = optax.apply_updates(params, updates)
      ...   print('Objective function: {:.2E}'.format(fn(params, x, y)))
      Objective function: 3.86E+01
      Objective function: 2.50E+01
      Objective function: 1.34E+01
      Objective function: 5.87E+00
      Objective function: 5.81E+00

    A similar example, but with a non-stochastic function where we can reuse
    the value and the gradient computed at the end of the linesearch:

      >>> import optax
      >>> import jax
      >>> import jax.numpy as jnp
      >>> # Function without extra arguments
      >>> def fn(params): return jnp.sum(params ** 2)
      >>> params = jnp.array([1., 2., 3.])
      >>> # In this case we can store value and grad with the store_grad field
      >>> # and reuse them using optax.value_and_grad_state_from_state
      >>> solver = optax.chain(
      ...    optax.sgd(learning_rate=1.),
      ...    optax.scale_by_backtracking_linesearch(
      ...        max_backtracking_steps=15, store_grad=True
      ...    )
      ... )
      >>> opt_state = solver.init(params)
      >>> print('Objective function: {:.2E}'.format(fn(params)))
      Objective function: 1.40E+01
      >>> value_and_grad = optax.value_and_grad_from_state(fn)
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

  References:
    Vaswani et al., `Painless Stochastic Gradient
    <https://arxiv.org/abs/1905.09997>`_, 2019

    Nocedal & Wright, `Numerical Optimization
    <https://doi.org/10.1007/978-0-387-40065-5>`_, 1999


  .. warning::
    The sufficient decrease criterion might be impossible to satisfy for some
    update directions. To guarantee a non-trivial solution for the sufficient
    decrease criterion, a descent direction for updates (:math:`u`) is required.
    An update (:math:`u`) is considered a descent direction if the derivative of
    :math:`f(w + \eta u)` at :math:`\eta = 0`
    (i.e.,  :math:`\langle u, \nabla f(w)\rangle`) is negative.  This condition
    is automatically satisfied when using :func:`optax.sgd` (without momentum),
    but may not hold true for other optimizers like :func:`optax.adam`.


    More generally, when chained with other transforms as
    ``optax.chain(opt_1, ..., opt_k,
    scale_by_backtraking_linesearch(max_backtracking_steps=...),
    opt_kplusone, ..., opt_n)``, the updates returned by chaining
    ``opt_1, ..., opt_k`` must be a descent direction. However, any transform
    after the backtracking line-search doesn't necessarily need to satisfy the
    descent direction property (one could for example use momentum).

  .. note:: The algorithm can support complex inputs.

  .. seealso:: :func:`optax.value_and_grad_from_state` to make this method
    more efficient for non-stochastic objectives.

  .. versionadded:: 0.2.0
  """

  def init_fn(params: base.Params) -> ScaleByBacktrackingLinesearchState:
    if store_grad:
      grad = optax.tree.zeros_like(params)
    else:
      grad = None
    # base output type on params type, except only real part if complex
    placeholder = jnp.empty((), dtype=jax.tree.leaves(params)[0].dtype)
    val_dtype = jnp.real(placeholder).real.dtype
    return ScaleByBacktrackingLinesearchState(
        learning_rate=jnp.array(1.0, dtype=val_dtype),
        value=jnp.array(jnp.inf, dtype=val_dtype),
        grad=grad,
        info=BacktrackingLinesearchInfo(
            num_linesearch_steps=jnp.asarray(0),
            decrease_error=jnp.array(jnp.inf, dtype=val_dtype),
        ),
    )

  def _compute_decrease_error(
      stepsize: jax.typing.ArrayLike,
      slope: jax.typing.ArrayLike,
      value: jax.typing.ArrayLike,
      new_value: jax.typing.ArrayLike,
  ) -> jax.typing.ArrayLike:
    decrease_error = (
        new_value - (1.0 + rtol) * value - stepsize * slope_rtol * slope
    )
    decrease_error = jnp.where(
        jnp.isnan(decrease_error), jnp.inf, decrease_error
    )
    return jnp.maximum(decrease_error, 0.0)

  def update_fn(
      updates: base.Updates,
      state: ScaleByBacktrackingLinesearchState,
      params: base.Params,
      *,
      value: jax.typing.ArrayLike,  # float
      grad: base.Updates,
      value_fn: Callable[..., jax.typing.ArrayLike],
      **extra_args: dict[str, Any],
  ) -> tuple[base.Updates, ScaleByBacktrackingLinesearchState]:
    """Compute scaled updates guaranteeing decrease of current objective.

    Args:
      updates: current updates.
      state: current state.
      params: current parameters.
      value: value of the function at the current params.
      grad: gradient of the function at the current params.
      value_fn: function returning the value of the function we seek to
        optimize.
      **extra_args: additional keyword arguments, if the function needs
        additional arguments such as input data, they should be put there, see
        the example in the docstring of the transform.

    Returns:
      updates: updates for the params (new_params = params + updates).
      state: updated state.

    .. warning:: The objective to minimize, ``value_fn``, can take more than
        one input, but must return a single scalar (float or jax.Array of
        dimension one). If the function requires more than one input, the
        additional inputs need to be fed to the update, see the example in the
        docstring of the transform. The function value_fn needs to be amenable
        to differentiation in JAX.
    """
    # Fetch arguments to be fed to value_fn from the extra_args
    (fn_kwargs,), remaining_kwargs = _extract_fns_kwargs(
        (value_fn,), extra_args
    )

    if remaining_kwargs:
      raise TypeError(
          "Unexpected keyword arguments passed to "
          "`scale_by_backtracking_linesearch.update`. "
          f"These arguments were not consumed by `value_fn`: "
          f"{sorted(remaining_kwargs.keys())}. "
          "Ensure that all extra keyword arguments are accepted "
          "by `value_fn`."
      )

    # Slope of lr -> value_fn(params + lr * updates) at lr = 0
    # Should be negative to ensure that there exists a lr (potentially
    # infinitesimal) that satisfies the criterion.
    slope = optax.tree.real(optax.tree.vdot(updates, optax.tree.conj(grad)))

    def cond_fn(
        search_state: BacktrackingLineSearchState,
    ):
      """Whether to stop the line-search inner loop."""
      decrease_error = search_state.decrease_error
      iter_num = search_state.iter_num
      return (~(decrease_error <= atol)) & (iter_num <= max_backtracking_steps)

    def body_fn(
        search_state: BacktrackingLineSearchState,
    ) -> BacktrackingLineSearchState:
      """Line-search inner loop step."""
      learning_rate = search_state.learning_rate
      new_grad = search_state.new_grad
      iter_num = search_state.iter_num
      # We start decreasing the learning rate after the first iteration
      # and up until the criterion is satisfied.
      learning_rate = jnp.where(
          iter_num > 0, decrease_factor * learning_rate, learning_rate
      )
      new_params = optax.tree.add_scale(params, learning_rate, updates)

      value_fn_ = functools.partial(value_fn, **fn_kwargs)
      if store_grad:
        # We evaluate value_fn and get its jvp operator so that we can
        # compute the gradient by transposing the jvp.
        new_value, jvp_value_fn = jax.linearize(value_fn_, new_params)

        decrease_error = _compute_decrease_error(
            learning_rate, slope, value, new_value
        )
        # If the line-search ends, we get the gradient for the new round of
        # line-search.
        new_grad = jax.lax.cond(
            (decrease_error <= atol) | (iter_num == max_backtracking_steps),
            lambda p: jax.linear_transpose(jvp_value_fn, p)(1.0)[0],
            lambda *_: new_grad,
            new_params,
        )
      else:
        # Here we just compute the value and leave the gradient as is
        new_value = value_fn_(new_params)
        decrease_error = _compute_decrease_error(
            learning_rate, slope, value, new_value
        )
      new_search_state = BacktrackingLineSearchState(
          learning_rate=learning_rate,
          new_value=new_value,
          new_grad=new_grad,
          decrease_error=decrease_error,
          iter_num=iter_num + 1,
      )
      return optax.tree.cast_like(new_search_state, other_tree=search_state)

    # We start with a guess candidate learning rate that may be larger than
    # the current one but no larger than the maximum one.
    learning_rate = jnp.minimum(
        increase_factor * state.learning_rate, max_learning_rate
    )
    search_state = BacktrackingLineSearchState(
        learning_rate=learning_rate,
        new_value=value,
        new_grad=optax.tree.zeros_like(params),
        decrease_error=jnp.array(jnp.inf),
        iter_num=0,
    )
    search_state = jax.lax.while_loop(cond_fn, body_fn, search_state)

    # If store_grad is False we simply return None (to not mix up with
    # optax.tree.zeros_like(params))
    new_grad = search_state.new_grad if store_grad else None
    new_value = search_state.new_value
    # If the decrease error is infinite, we avoid making any step (which would
    # result in nan or infinite values): we set the learning rate to 0.
    new_learning_rate = jnp.where(
        jnp.isinf(search_state.decrease_error), 0.0, search_state.learning_rate
    )

    if verbose:
      # We print information only if the linesearch failed.
      _cond_print(
          search_state.decrease_error > atol,
          "INFO: optax.scale_by_backtracking_linesearch:\n"
          "Backtracking linesearch failed to find a stepsize ensuring sufficent"
          " decrease.\n"
          "Value at current params: {value},\n"
          "Slope along update direction: {slope}\n"
          "Stepsize: {stepsize}\n"
          "Decrease Error: {decrease_error}",
          stepsize=search_state.learning_rate,
          decrease_error=search_state.decrease_error,
          value=value,
          slope=slope,
      )
      _cond_print(
          jnp.isinf(search_state.decrease_error),
          "Using a stepsize of 0 to avoid infinite or nan values.",
      )
    # At the end, we just scale the updates with the learning rate found.
    new_updates = optax.tree.scale(new_learning_rate, updates)
    info = BacktrackingLinesearchInfo(
        num_linesearch_steps=search_state.iter_num,
        decrease_error=search_state.decrease_error,
    )
    new_state = ScaleByBacktrackingLinesearchState(
        learning_rate=new_learning_rate,
        value=new_value,
        grad=new_grad,
        info=info,
    )

    return new_updates, optax.tree.cast_like(new_state, other_tree=state)

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

