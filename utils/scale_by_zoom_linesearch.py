
def scale_by_zoom_linesearch(
    max_linesearch_steps: jax.typing.ArrayLike,  # int
    max_learning_rate: Optional[jax.typing.ArrayLike] = None,  # float
    tol: jax.typing.ArrayLike = 0.0,
    increase_factor: jax.typing.ArrayLike = 2.0,
    slope_rtol: jax.typing.ArrayLike = 1e-4,
    curv_rtol: jax.typing.ArrayLike = 0.9,
    approx_dec_rtol: Optional[jax.typing.ArrayLike] = 1e-6,
    stepsize_precision: jax.typing.ArrayLike = 1e-5,
    initial_guess_strategy: str = "keep",
    verbose: bool = False,
) -> base.GradientTransformationExtraArgs:
  r"""Linesearch ensuring sufficient decrease and small curvature.

  This algorithm searches for a learning rate, a.k.a. stepsize, that satisfies
  both a sufficient decrease criterion, a.k.a. Armijo-Goldstein criterion,

  .. math::
    f(w + \eta u) \leq f(w) + \eta c_1 \langle u, \nabla f(w) \rangle + \epsilon
    \,,

  and a small curvature (along the update direction) criterion, a.k.a.
  Wolfe or second Wolfe criterion,

  .. math::
    |\langle \nabla f(w + \eta u), u \rangle| \leq c_2 |\langle \nabla f(w),
    \rangle| + \epsilon\,,

  where

  - :math:`f` is the function to minimize,
  - :math:`w` are the current parameters,
  - :math:`\eta` is the learning rate to find,
  - :math:`u` is the update direction,
  - :math:`c_1` is a coefficient (``slope_rtol``) measuring the relative
    decrease of the function in terms of the slope (scalar product between
    the gradient and the updates),
  - :math:`c_2` is a coefficient (``curv_rtol``) measuring the relative
    decrease of curvature.
  - :math:`\epsilon` is an absolute tolerance (``tol``).

  To deal with very flat functions, this linesearch switches from the sufficient
  decrease criterion presented above to an approximate sufficient decrease
  criterion introduced by Hager and Zhang (see [Hager and Zhang, 2006]).

  .. math::
    |\langle \nabla f(w+\eta u), u \rangle| \leq (2 c_1 - 1) |\langle \nabla
    f(w), \rangle| + \epsilon\,.

  The approximate curvature criterion is taken only if the values tried by the
  linesearch fall below a relative decrease of the initial function, that is,

  .. math::
    f(w + \eta u) \leq f(w) + c_3 |f(w)|

  where :math:`c_3` is a coefficient ``approx_dec_rtol`` measuring the relative
  decrease of the objective (see reference below and comments in the code for
  more details).

  The original sufficient decrease criterion can only capture
  differences up to :math:`\sqrt{\varepsilon_{machine}}` while the approximate
  sufficient decrease criterion can capture differences up to
  :math:`\varepsilon_{machine}` (see [Hager and Zhang, 2006]).
  Note that this add-on is not part of the original implementation of
  [Nocedal and Wright, 1999] and can be removed by
  setting ``approx_dec_rtol`` to ``None``.

  Args:
    max_linesearch_steps: maximum number of linesearch iterations.
    max_learning_rate: maximum admissible learning rate. Can be set to ``None``
      for no upper bound. A non ``None`` value may prevent the linesearch to
      find a learning rate satisfying the small curvature criterion, since the
      latter may require sufficiently large stepsizes.
    tol: tolerance on the criterions.
    increase_factor: increasing factor to augment the learning rate when
      searching for a valid interval containing a learning rate satisfying both
      criterions.
    slope_rtol: relative tolerance for the slope in the sufficient decrease
      criterion.
    curv_rtol: relative tolerance for the curvature in the small curvature
      criterion.
    approx_dec_rtol: relative tolerance for the initial value in the approximate
      sufficient decrease criterion. Can be set to ``None`` to use only the
      original Armijo-Goldstein decrease criterion.
    stepsize_precision: precision in the search of a stepsize satisfying both
      conditions. The algorithm proceeds with a bisection that refines an
      interval containing a stepsize satisfying both conditions. If that
      interval is reduced below ``stepsize_precision`` and a stepsize satisfying
      a sufficient decrease has been found, the algorithm selects that stepsize
      even if the curvature condition is not satisfied.
    initial_guess_strategy: initial guess for the learning rate used to start
      the linesearch. Can be either ``one`` or ``keep``. If ``one``, the initial
      guess is set to 1. If ``keep``, the initial guess is set to the learning
      rate of the previous step. We recommend to use ``keep`` if this linesearch
      is used in combination with SGD. We recommend to use ``one`` if this
      linesearch is used in combination with Newton methods or quasi-Newton
      methods such as L-BFGS.
    verbose: whether to print additional debugging information in case the
      linesearch fails.

  Returns:
    A :class:`optax.GradientTransformationExtraArgs` object consisting in
    an init and an update function.

  Examples:
    An example on using the zoom line-search with SGD::

      >>> import optax
      >>> import jax
      >>> import jax.numpy as jnp
      >>> solver = optax.chain(
      ...    optax.sgd(learning_rate=1.),
      ...    optax.scale_by_zoom_linesearch(max_linesearch_steps=15)
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
      Objective function: 2.56E-13
      Objective function: 2.84E-14
      Objective function: 0.00E+00
      Objective function: 0.00E+00
      Objective function: 0.00E+00

    A similar example, but with a non-stochastic function where we can reuse
    the value and the gradient computed at the end of the linesearch:

      >>> import optax
      >>> import jax
      >>> import jax.numpy as jnp
      >>> # Function without extra arguments
      >>> def fn(params): return jnp.sum(params ** 2)
      >>> params = jnp.array([1., 2., 3.])
      >>> solver = optax.chain(
      ...    optax.sgd(learning_rate=1.),
      ...    optax.scale_by_zoom_linesearch(max_linesearch_steps=15)
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
      Objective function: 0.00E+00
      Objective function: 0.00E+00
      Objective function: 0.00E+00
      Objective function: 0.00E+00
      Objective function: 0.00E+00

  References:
    Algorithms 3.5 3.6 of Nocedal and Wright, `Numerical Optimization
    <https://doi.org/10.1007/978-0-387-40065-5>`_, 1999

    Hager and Zhang `Algorithm 851: CG_DESCENT, a Conjugate Gradient Method
    with Guaranteed Descent
    <https://doi.org/10.1145/1132973.1132979>`_, 2006

  .. note::
    The curvature criterion can be avoided by setting by setting
    ``curv_rtol=jnp.inf``. The resulting algorithm will amount to a
    backtracking linesearch where a point satisfying sufficient decrease is
    searched by minimizing a quadratic or cubic approximation of the objective.
    This can be sufficient in practice and avoids having the linesearch spend
    many iterations trying to satisfy the small curvature criterion.

  .. note:: The algorithm can support complex inputs.

  .. seealso:: :func:`optax.value_and_grad_from_state` to make this method
    more efficient for non-stochastic objectives.
  """

  # Instantiates the linesearch with the given arguments.
  init_ls, step_ls, cond_step_ls = zoom_linesearch(
      max_linesearch_steps=max_linesearch_steps,
      max_stepsize=max_learning_rate,
      tol=tol,
      increase_factor=increase_factor,
      slope_rtol=slope_rtol,
      curv_rtol=curv_rtol,
      approx_dec_rtol=approx_dec_rtol,
      interval_threshold=stepsize_precision,
      verbose=verbose,
  )

  def init_fn(params: base.Params) -> ScaleByZoomLinesearchState:
    """Initializes state of scale_by_zoom_linesearch."""
    placeholder = jnp.empty((), jax.tree.leaves(params)[0].dtype)
    val_dtype = jnp.real(placeholder).dtype
    return ScaleByZoomLinesearchState(
        learning_rate=jnp.asarray(1.0, dtype=val_dtype),
        value=jnp.asarray(jnp.inf, dtype=val_dtype),
        grad=optax.tree.zeros_like(params),
        info=ZoomLinesearchInfo(
            num_linesearch_steps=jnp.asarray(0),
            decrease_error=jnp.asarray(jnp.inf),
            curvature_error=jnp.asarray(jnp.inf),
        ),
    )

  def update_fn(
      updates: base.Updates,
      state: ScaleByZoomLinesearchState,
      params: base.Params,
      *,
      value: jax.typing.ArrayLike,
      grad: base.Updates,
      value_fn: Callable[..., tuple[jax.typing.ArrayLike, base.Updates]],
      **extra_args: dict[str, Any],
  ) -> tuple[base.Updates, ScaleByZoomLinesearchState]:
    """Scales updates using the zoom linesearch.

    Args:
      updates: current updates.
      state: current state.
      params: current parameters.
      value: value of the function at the current params.
      grad: gradient of the function at the current params.
      value_fn: function returning the value of the function we seek to
        optimize.
      **extra_args: additional keyword arguments, if the function needs
        additional arguments such as input data, they should be put there.

    Returns:
      updates: updates for the params (new_params = params + updates).
      state: updated state.

    .. warning:: The objective to minimize, ``value_fn``, can take more than
        one input, but must return a single scalar (``float`` or scalar
        ``jax.Array``). If the function requires more than one input, the
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
          "`scale_by_zoom_linesearch.update`. "
          f"These arguments were not consumed by `value_fn`: "
          f"{sorted(remaining_kwargs.keys())}. "
          "Ensure that all extra keyword arguments are accepted "
          "by `value_fn`."
      )

    value_and_grad_fn = jax.value_and_grad(value_fn)

    init_state = init_ls(
        updates,
        params,
        value=value,
        grad=grad,
        prev_stepsize=state.learning_rate,
        initial_guess_strategy=initial_guess_strategy,
    )

    final_state = jax.lax.while_loop(
        cond_step_ls,
        functools.partial(
            step_ls,
            value_and_grad_fn=value_and_grad_fn,
            fn_kwargs=fn_kwargs,
        ),
        init_state,
    )
    learning_rate = final_state.stepsize
    scaled_updates = optax.tree.scale(learning_rate, updates)
    info_step = ZoomLinesearchInfo(
        num_linesearch_steps=final_state.count,
        decrease_error=final_state.decrease_error,
        curvature_error=final_state.curvature_error,
    )
    new_state = ScaleByZoomLinesearchState(
        learning_rate=learning_rate,
        value=final_state.value,
        grad=final_state.grad,
        info=info_step,
    )
    return scaled_updates, optax.tree.cast_like(new_state, other_tree=state)

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

