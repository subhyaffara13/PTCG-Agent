import functools
from typing import Any, Callable, Optional

def zoom_linesearch(
    max_linesearch_steps: jax.typing.ArrayLike,  # int
    max_stepsize: Optional[jax.typing.ArrayLike] = None,  # float
    tol: jax.typing.ArrayLike = 0.0,
    increase_factor: jax.typing.ArrayLike = 2.0,
    slope_rtol: jax.typing.ArrayLike = 1e-4,
    curv_rtol: jax.typing.ArrayLike = 0.9,
    approx_dec_rtol: Optional[jax.typing.ArrayLike] = 1e-6,
    interval_threshold: jax.typing.ArrayLike = 1e-5,
    verbose: bool = False,
) -> tuple[
    Callable[..., ZoomLinesearchState],
    Callable[..., ZoomLinesearchState],
    Callable[..., jax.typing.ArrayLike],
]:
  r"""Zoom Linesearch ensuring sufficient decrease and small curvature.

  This linesearch algorithm finds a step size that satisfies both a
  sufficient decrease criterion and a small curvature criterion.
  See :func:`optax.scale_by_zoom_linesearch`
  for a detailed mathematical description of these criteria.

  The algorithm proceeds in two phases:

  1. **Interval Search:**
    Finds an upper bound :math:`\bar\eta` on the step size such that there
    exists a step size :math:`\eta \in [0, \bar\eta]` satisfying both criteria.

  2. **Zoom (Bisection):**
    Searches within the initial interval to find a suitable step size.
    This phase uses a bisection-like method, informed by the problem properties
    and criteria. It iteratively narrows the interval until a satisfactory step
    size is found.

  Args:
    max_linesearch_steps: maximum number of linesearch iterations.
    max_stepsize: maximal admissible learning rate. Can be set to ``None`` for
      no upper bound. An inappropriate value may prevent the linesearch to find
      a learning rate satisfying the small curvature criterion, since the latter
      may require sufficiently large stepsizes.
    tol: tolerance on the criterions.
    increase_factor: increasing factor to augment the learning rate when
      searching for an initial valid interval (1st phase above).
    slope_rtol: relative tolerance for the slope in the sufficient decrease
      criterion, see :func:`optax.scale_by_zoom_linesearch`.
    curv_rtol: relative tolerance for the curvature in the small curvature
      criterion, see :func:`optax.scale_by_zoom_linesearch`.
    approx_dec_rtol: relative tolerance for the initial value in the approximate
      sufficient decrease criterion. Can be set to ``None`` to use only the
      Armijo-Goldstein decrease criterion, see
      :func:`optax.scale_by_zoom_linesearch`.
    interval_threshold: if the size of the interval searched is below this
      threshold and a sufficient decrease for some stepsize has been found, then
      the linesearch selects the stepsize and ends.
    verbose: whether to print debugging information if the linesearch fails.

  Returns:
    tuple (``init_fn``, ``step_fn``, ``cond_step_fn``) where

    * ``init_fn(updates, params, *, value, grad, stepsize_guess) ->
      ZoomLinesearchState``
      initializes the state of the linesearch given the current
      parameters ``params``, the ``updates`` direction, the ``value`` of the
      function at the ``params``, the gradient ``grad`` of the function at
      ``params
    * ``step_fn(state, value_and_grad_fn, fn_kwargs) -> ZoomLinesearchState``
      updates the state of the linesearch given the current ``state``, a
      function ``value_and_grad_fn`` returning the value and the gradient of the
      function at any given inputs, ``fn_kwargs`` additional keyword-only
      arguments to be passed to the function (other than parameters, it could be
      additional data for example)
    * ``cond_step_fn(state) -> bool`` returns a boolean indicating whether the
      linesearch iterations should continue (``True``) or not (``False``).

  References:
    Algorithms 3.5 3.6 of Nocedal and Wright, `Numerical Optimization
    <https://doi.org/10.1007/978-0-387-40065-5>`_, 1999

    Hager and Zhang `Algorithm 851: CG_DESCENT, a Conjugate Gradient Method
    with Guaranteed Descent
    <https://doi.org/10.1145/1132973.1132979>`_, 2006
  """

  def _value_and_slope_on_line(
      value_and_grad_fn: Callable[
          ..., tuple[jax.typing.ArrayLike, base.Updates]],
      params: base.Params,
      stepsize: jax.typing.ArrayLike,
      updates: base.Updates,
      fn_kwargs,
  ) -> tuple[
      base.Params, jax.typing.ArrayLike, base.Updates, jax.typing.ArrayLike]:
    r"""Compute value and slope on line.

    Mathematically, outputs

    .. math::
      (w_\eta, f(w_\eta; x), \nabla f(w_\eta; x), \partial f(w_\eta; x)(u)

    for :math:`w_\eta = w + \eta u`,
    where
      - :math:`w` are the current parameters ``params``,
      - :math:`u` is the update direction ``updates``,
      - :math:`\eta` is the stepsize, a.k.a. learning rate, ``stepsize``,
      - :math:`x` are additional arguments to the function ``fn_kwargs``,
      - :math:`\nabla f(w_\eta; x)` is the gradient of :math:`f(\cdot; x)`
        at the new step, :math:`w_eta`,
      - :math:`\partial f(w_\eta; x)(u)` is the directional derivative of
        :math:`f(\cdot; x)` at :math:`w_\eta` in the direction :math:`u`,
        that is, the slope (derivative) of
        :math:`\eta \rightarrow f(w + \eta u)` at :math:`\eta`.
        So :math:`\partial f(w_\eta; x)(u) = \nabla f(w_\eta)^\top u`.

    Args:
      value_and_grad_fn: function returning value and gradient at given inputs
      params: current parameters
      stepsize: tentative stepsize taken
      updates: direction along which the step is taken
      fn_kwargs: additional arguments to be passed to the function

    Returns:
      ``(step, value_step, grad_step, slope_step)``
      where

        * ``step`` are the parameters at the selected stepsize,
        * ``value_step`` is the value at the step,
        * ``grad_step`` is the gradient at the step,
        * ``slope_step`` is the derivative of the function in terms of the
          stepsize at the step.
    """
    step = optax.tree.add_scale(params, stepsize, updates)
    value_step, grad_step = value_and_grad_fn(step, **fn_kwargs)
    slope_step = optax.tree.real(
        optax.tree.vdot(optax.tree.conj(grad_step), updates)
    )
    return step, value_step, grad_step, slope_step

  def _compute_decrease_error(
      stepsize: jax.typing.ArrayLike,
      value_step: jax.typing.ArrayLike,
      slope_step: jax.typing.ArrayLike,
      value_init: jax.typing.ArrayLike,
      slope_init: jax.typing.ArrayLike,
  ) -> jax.typing.ArrayLike:
    """Compute decrease error."""
    # We consider either the usual sufficient decrease (Armijo criterion), see
    # equation (3.7a) of [Nocedal and Wright, 1999]
    decrease_error = (
        value_step - value_init - slope_rtol * stepsize * slope_init
    )
    if approx_dec_rtol is not None:
      # or an approximate decrease criterion, see equation (23) of
      # [Hager and Zhang, 2006].
      approx_decrease_error = slope_step - (2 * slope_rtol - 1.0) * slope_init

      # The classical Armijo criterion may fail to be satisfied if we are too
      # close to a minimum, causing the optimizer to fail as explained in
      # [Hager and Zhang, 2006].

      # We switch to the approximate decrease criterion only if we are close
      # enough to the minimizer. To measure this we check whether the
      # new value is smaller than the initial one up to a tolerance of
      # the order of magnitude of the initial value (see equations (26) and
      # (27) of [Hager and Zhang, 2006] that we simplify using one iterate in
      # equation (26)).
      delta_values = (
          value_step - value_init - approx_dec_rtol * jnp.abs(value_init)
      )
      approx_decrease_error = jnp.maximum(approx_decrease_error, delta_values)
      # We take then the *minimum* of both errors.
      decrease_error = jnp.minimum(approx_decrease_error, decrease_error)

    # We only care whether the criterion is violated (larger than 0.0) and
    # take care of potential nan values by converting to inf
    decrease_error = jnp.maximum(decrease_error, 0.0)
    decrease_error = jnp.where(
        jnp.isnan(decrease_error), jnp.inf, decrease_error
    )
    return decrease_error

  def _compute_curvature_error(
      slope_step: jax.typing.ArrayLike, slope_init: jax.typing.ArrayLike
  ) -> jax.typing.ArrayLike:
    """Compute curvature error."""
    # See equation (3.7b) of [Nocedal and Wright, 1999].
    curvature_error = jnp.abs(slope_step) - curv_rtol * jnp.abs(slope_init)

    # We only care whether the criterion is violated (larger than 0.0) and
    # take care of potential nan values by converting to inf
    curvature_error = jnp.maximum(curvature_error, 0.0)
    curvature_error = jnp.where(
        jnp.isnan(curvature_error), jnp.inf, curvature_error
    )
    return curvature_error

  def _try_safe_step(
      state: ZoomLinesearchState,
  ) -> ZoomLinesearchState:
    """Try making a step with stepsize ensuring at least sufficient decrease."""
    outside_domain = jnp.isinf(state.decrease_error)
    final_stepsize, final_value, final_grad = optax.tree.where(
        (state.safe_stepsize > 0.0) | outside_domain,
        [state.safe_stepsize, state.safe_value, state.safe_grad],
        [state.stepsize, state.value, state.grad],
    )
    if verbose:
      jax.debug.print(
          "INFO: optax.scale_by_zoom_linesearch:\n"
          "Value at current params: {value_init}\n"
          "Slope along update direction: {slope_init}\n"
          "Stepsize reached: {stepsize}\n"
          "Decrease Error: {decrease_error}\n"
          "Curvature Error: {curvature_error}",
          value_init=state.value_init,
          slope_init=state.slope_init,
          stepsize=state.stepsize,
          decrease_error=state.decrease_error,
          curvature_error=state.curvature_error,
          ordered=True,
      )
      interval_length = jnp.abs(state.low - state.high)
      too_small_int = interval_length <= interval_threshold
      _cond_print(
          too_small_int,
          FLAG_INTERVAL_TOO_SMALL + " Interval length: {interval_length}.",
          interval_length=interval_length,
      )
      jax.lax.cond(
          state.safe_stepsize > 0.0,
          lambda _: jax.debug.print(
              FLAG_CURVATURE_COND_NOT_SATISFIED
              + " Stepsize ensuring sufficient decrease: {safe_stepsize}.",
              safe_stepsize=state.safe_stepsize,
          ),
          _failure_diagnostic,
          state,
      )
    final_state = state._replace(
        stepsize=final_stepsize, grad=final_grad, value=final_value
    )
    return optax.tree.cast_like(final_state, other_tree=state)

  def _search_interval(
      state: ZoomLinesearchState,
      value_and_grad_fn: Callable[
          ..., tuple[jax.typing.ArrayLike, base.Updates]],
      fn_kwargs: dict[str, Any],
  ) -> ZoomLinesearchState:
    """Search initial interval, Algorithm 3.5 of [Nocedal and Wright, 1999]."""

    iter_num = state.count

    params = state.params
    updates = state.updates
    stepsize_guess = state.stepsize_guess

    value_init = state.value_init
    slope_init = state.slope_init

    prev_stepsize = state.stepsize
    prev_value_step = state.value
    prev_slope_step = state.slope

    safe_stepsize = state.safe_stepsize
    safe_value = state.safe_value
    safe_grad = state.safe_grad

    # Choose new point, larger than previous one or set to initial guess
    # for first iteration.
    larger_stepsize = increase_factor * prev_stepsize
    new_stepsize = jnp.where(iter_num == 0, stepsize_guess, larger_stepsize)
    if max_stepsize is not None:
      max_stepsize_reached = new_stepsize >= max_stepsize
      new_stepsize = jnp.minimum(new_stepsize, max_stepsize)
    else:
      max_stepsize_reached = jnp.asarray(False)

    _, new_value_step, new_grad_step, new_slope_step = _value_and_slope_on_line(
        value_and_grad_fn, params, new_stepsize, updates, fn_kwargs
    )

    decrease_error = _compute_decrease_error(
        new_stepsize, new_value_step, new_slope_step, value_init, slope_init
    )
    curvature_error = _compute_curvature_error(new_slope_step, slope_init)
    new_error = jnp.maximum(decrease_error, curvature_error)

    # If the new point satisfies at least the decrease error we keep it
    # in case the curvature error cannot be satisfied.
    safe_decrease = decrease_error <= tol
    new_safe_stepsize, new_safe_value, new_safe_grad = optax.tree.where(
        safe_decrease,
        [new_stepsize, new_value_step, new_grad_step],
        [safe_stepsize, safe_value, safe_grad],
    )

    # If the new point is not good, set high and low values according to
    # conditions described in Algorithm 3.5 of [Nocedal and Wright, 1999]
    set_high_to_new = (decrease_error > 0.0) | (
        (new_value_step >= prev_value_step) & (iter_num > 0)
    )
    set_low_to_new = (new_slope_step >= 0.0) & (~set_high_to_new)

    # By default we set high to new and correct if we should have set
    # low to new. If none should have set, the search for the interval
    # continues anyway.
    low_, value_low_, slope_low_, high_, value_high_, slope_high_ = (
        prev_stepsize,
        prev_value_step,
        prev_slope_step,
        new_stepsize,
        new_value_step,
        new_slope_step,
    )

    default = [low_, value_low_, slope_low_, high_, value_high_, slope_high_]
    candidate = [
        new_stepsize,
        new_value_step,
        new_slope_step,
        prev_stepsize,
        prev_value_step,
        prev_slope_step,
    ]
    [low, value_low, slope_low, high, value_high, slope_high] = (
        optax.tree.where(set_low_to_new, candidate, default)
    )

    # If high or low have been set or the point is good, the interval has been
    # found. Otherwise, we'll keep on augmenting the stepsize.
    interval_found = set_high_to_new | set_low_to_new | (new_error <= tol)

    # If new_error <= tol, the line search is done. If the maximal stepsize
    # is reached, either an interval has been found and we will zoom into this
    # interval or no interval has been found meaning that the maximal stepsize
    # satisfies the Armijo criterion but a priori not the curvature criterion.
    # In that case there is no hope to satisfy the curvature criterion as it
    # would a priori be found for a larger stepsize, so we simply take the
    # maximal stepsize and flag that we could not satisfy the curvature
    # criterion.
    done = (new_error <= tol) | (max_stepsize_reached & ~interval_found)
    if verbose:
      _cond_print(
          (max_stepsize_reached & ~interval_found),
          "INFO: optax.scale_by_zoom_linesearch:\n"
          "Value at current params: {value_init}\n"
          "Slope along update direction: {slope_init}\n"
          "Stepsize reached: {stepsize}\n"
          "Decrease Error: {decrease_error}\n"
          "Curvature Error: {curvature_error}"
          + FLAG_INTERVAL_NOT_FOUND
          + "\n"
          + FLAG_CURVATURE_COND_NOT_SATISFIED,
          value_init=value_init,
          slope_init=slope_init,
          stepsize=new_stepsize,
          decrease_error=decrease_error,
          curvature_error=curvature_error,
      )
    failed = (iter_num + 1 >= max_linesearch_steps) & (~done)

    new_state = ZoomLinesearchState(
        count=numerics.safe_increment(iter_num),
        #
        params=params,
        updates=updates,
        stepsize_guess=stepsize_guess,
        #
        stepsize=new_stepsize,
        value=new_value_step,
        grad=new_grad_step,
        slope=new_slope_step,
        #
        value_init=value_init,
        slope_init=slope_init,
        #
        decrease_error=decrease_error,
        curvature_error=curvature_error,
        error=new_error,
        #
        interval_found=jnp.asarray(interval_found),
        done=jnp.asarray(done),
        failed=jnp.asarray(failed),
        #
        low=low,
        value_low=value_low,
        slope_low=slope_low,
        high=high,
        value_high=value_high,
        slope_high=slope_high,
        cubic_ref=low,
        value_cubic_ref=value_low,
        #
        safe_stepsize=new_safe_stepsize,
        safe_value=new_safe_value,
        safe_grad=new_safe_grad,
    )
    return optax.tree.cast_like(new_state, other_tree=state)

  def _zoom_into_interval(
      state: ZoomLinesearchState,
      value_and_grad_fn: Callable[
          ..., tuple[jax.typing.ArrayLike, base.Updates]],
      fn_kwargs: dict[str, Any],
  ) -> ZoomLinesearchState:
    """Zoom procedure, Algorithm 3.6 of [Nocedal and Wright, 1999]."""

    iter_num = state.count

    params = state.params
    updates = state.updates

    value_init = state.value_init
    slope_init = state.slope_init

    low = state.low
    value_low = state.value_low
    slope_low = state.slope_low
    high = state.high
    value_high = state.value_high
    slope_high = state.slope_high
    cubic_ref = state.cubic_ref
    value_cubic_ref = state.value_cubic_ref

    safe_stepsize = state.safe_stepsize
    safe_value = state.safe_value
    safe_grad = state.safe_grad

    # Check if interval not too small otherwise fail
    delta = jnp.abs(high - low)
    left = jnp.minimum(high, low)
    right = jnp.maximum(high, low)
    cubic_chk = 0.2 * delta
    quad_chk = 0.1 * delta

    # We use rather large values of interval threshold compared to machine
    # precision such that we avoid wasting iterations to satisfy curvature
    # criterion (a stepsize reducing values is taken if it exists when threshold
    # is met)
    too_small_int = delta <= interval_threshold

    # Find new point by interpolation
    middle_cubic = _cubicmin(
        low, value_low, slope_low, high, value_high, cubic_ref, value_cubic_ref
    )
    middle_cubic_valid = (middle_cubic > left + cubic_chk) & (
        middle_cubic < right - cubic_chk
    )
    use_cubic = middle_cubic_valid
    middle_quad = _quadmin(low, value_low, slope_low, high, value_high)
    middle_quad_valid = (middle_quad > left + quad_chk) & (
        middle_quad < right - quad_chk
    )
    use_quad = (~use_cubic) & middle_quad_valid
    middle_bisection = (low + high) / 2.0
    use_bisection = (~use_cubic) & (~use_quad)

    middle = jnp.where(use_cubic, middle_cubic, cubic_ref)
    middle = jnp.where(use_quad, middle_quad, middle)
    middle = jnp.where(use_bisection, middle_bisection, middle)

    # Check if new point is good
    _, value_middle, grad_middle, slope_middle = _value_and_slope_on_line(
        value_and_grad_fn, params, middle, updates, fn_kwargs
    )

    decrease_error = _compute_decrease_error(
        middle, value_middle, slope_middle, value_init, slope_init
    )
    curvature_error = _compute_curvature_error(slope_middle, slope_init)
    new_error = jnp.maximum(decrease_error, curvature_error)

    # If the new point satisfies at least the decrease error we keep it in case
    # the curvature error cannot be satisfied.
    # We take the one with the smallest value.
    safe_decrease = decrease_error <= tol
    update_safe_stepsize = safe_decrease & (value_middle < safe_value)
    new_safe_stepsize, new_safe_value, new_safe_grad = optax.tree.where(
        update_safe_stepsize,
        [middle, value_middle, grad_middle],
        [safe_stepsize, safe_value, safe_grad],
    )

    # If both Armijo and curvature criterions are satisfied, we are done.
    # In any case, we take the stepizes, value and grad computed at the new
    # middle point for the running state.
    done = new_error <= tol

    # Otherwise, we update high and low values
    set_high_to_middle = (decrease_error > 0.0) | (value_middle >= value_low)
    secant_interval = slope_middle * (high - low)
    set_high_to_low = (secant_interval >= 0.0) & (~set_high_to_middle)
    set_low_to_middle = ~set_high_to_middle

    # Set high to middle, or low, or keep as it is
    default = [high, value_high, slope_high]
    candidate = [middle, value_middle, slope_middle]
    [new_high_, new_value_high_, new_slope_high_] = optax.tree.where(
        set_high_to_middle, candidate, default
    )
    default = [new_high_, new_value_high_, new_slope_high_]
    candidate = [low, value_low, slope_low]
    [new_high, new_value_high, new_slope_high] = optax.tree.where(
        set_high_to_low, candidate, default
    )

    # Set low to middle or keep as it is
    default = [low, value_low, slope_low]
    candidate = [middle, value_middle, slope_middle]
    [new_low, new_value_low, new_slope_low] = optax.tree.where(
        set_low_to_middle, candidate, default
    )

    # Update cubic reference point.
    # If high changed then it can be used as the new ref point.
    # Otherwise, low has been updated and not kept as high
    # so it can be used as the new ref point.
    [new_cubic_ref, new_value_cubic_ref] = optax.tree.where(
        set_high_to_middle | set_high_to_low,
        [high, value_high],
        [low, value_low],
    )
    # We stop if the searched interval is reduced below machine precision
    # and we already have found a positive stepsize ensuring sufficient
    # decrease. If no stepsize with sufficient decrease has been found,
    # we keep going on (some extremely steep functions require very small
    # stepsizes, see zakharov test in linesearch_test.py)
    max_iter_reached = (iter_num + 1) >= max_linesearch_steps
    presumably_failed = jnp.asarray(max_iter_reached) | (
        too_small_int & (new_safe_stepsize > 0.0)
    )
    failed = presumably_failed & ~done
    new_state = ZoomLinesearchState(
        count=numerics.safe_increment(iter_num),
        #
        params=params,
        updates=updates,
        stepsize_guess=state.stepsize_guess,
        #
        stepsize=middle,
        value=value_middle,
        grad=grad_middle,
        slope=slope_middle,
        #
        value_init=value_init,
        slope_init=slope_init,
        #
        decrease_error=decrease_error,
        curvature_error=curvature_error,
        error=new_error,
        #
        interval_found=state.interval_found,  # unchanged at this stage
        done=done,
        failed=failed,
        #
        low=new_low,
        value_low=new_value_low,
        slope_low=new_slope_low,
        high=new_high,
        value_high=new_value_high,
        slope_high=new_slope_high,
        cubic_ref=new_cubic_ref,
        value_cubic_ref=new_value_cubic_ref,
        #
        safe_stepsize=new_safe_stepsize,
        safe_value=new_safe_value,
        safe_grad=new_safe_grad,
    )
    return optax.tree.cast_like(new_state, other_tree=state)

  def _failure_diagnostic(state: ZoomLinesearchState) -> None:
    """Prints failure diagnostics."""
    jax.debug.print(FLAG_NO_STEPSIZE_FOUND)
    stepsize = state.stepsize

    slope_init = state.slope_init
    is_descent_dir = slope_init < 0.0
    _cond_print(
        ~is_descent_dir,
        FLAG_NOT_A_DESCENT_DIRECTION
        + "The slope (={slope_init}) at stepsize=0 should be negative",
        slope_init=slope_init,
    )
    _cond_print(
        is_descent_dir,
        "Consider augmenting the maximal number of linesearch iterations.",
    )
    eps = jnp.finfo(jnp.float32).eps
    below_eps = stepsize < eps
    _cond_print(
        below_eps & is_descent_dir,
        "Computed stepsize (={stepsize}) "
        "is below machine precision (={eps}), "
        "consider passing to higher precision like x64, using "
        "jax.config.update('jax_enable_x64', True).",
        stepsize=stepsize,
        eps=eps,
    )
    abs_slope_init = jnp.abs(slope_init)
    high_slope = abs_slope_init > 1e16
    _cond_print(
        high_slope & is_descent_dir,
        "Very large absolute slope at stepsize=0. "
        "(|slope|={abs_slope_init}). "
        "The objective is badly conditioned. "
        "Consider reparameterizing objective (e.g., normalizing parameters) "
        "or finding a better guess for the initial parameters for the "
        "solver.",
        abs_slope_init=abs_slope_init,
    )
    outside_domain = jnp.isinf(state.decrease_error)
    _cond_print(
        outside_domain,
        "Cannot even make a step without getting Inf or Nan. "
        + "The linesearch won't make a step and the optimizer is stuck.",
    )
    _cond_print(
        ~outside_domain,
        "Making an unsafe step, not decreasing enough the objective. "
        "Convergence of the solver is compromised as it does not reduce"
        " values.",
    )

  def init_fn(
      updates: base.Updates,
      params: base.Params,
      *,
      value: jax.typing.ArrayLike,
      grad: base.Updates,
      prev_stepsize: jax.typing.ArrayLike = 1.0,
      initial_guess_strategy: str = "one",
  ) -> ZoomLinesearchState:
    """Initializes the linesearch state."""

    if initial_guess_strategy == "one":
      stepsize_guess = jnp.asarray(1.0)
    elif initial_guess_strategy == "keep":
      stepsize_guess = prev_stepsize
    else:
      raise ValueError(
          f"Unknown initial guess strategy: {initial_guess_strategy}"
      )
    placeholder = jnp.empty((), jax.tree.leaves(params)[0].dtype)
    val_dtype = jnp.real(placeholder).dtype
    slope = optax.tree.real(optax.tree.vdot(updates, grad))
    return ZoomLinesearchState(
        count=jnp.asarray(0),
        #
        params=params,
        updates=updates,
        stepsize_guess=stepsize_guess,
        #
        stepsize=jnp.asarray(0.0, dtype=val_dtype),
        value=jnp.array(value, dtype=val_dtype),
        grad=grad,
        slope=slope,
        #
        value_init=value,
        slope_init=slope,
        #
        decrease_error=jnp.asarray(jnp.inf),
        curvature_error=jnp.asarray(jnp.inf),
        error=jnp.asarray(jnp.inf),
        #
        interval_found=jnp.asarray(False),
        done=jnp.asarray(False),
        failed=jnp.asarray(False),
        #
        low=jnp.asarray(0.0),
        value_low=value,
        slope_low=slope,
        high=jnp.asarray(0.0),
        value_high=value,
        slope_high=slope,
        cubic_ref=jnp.asarray(0.0),
        value_cubic_ref=value,
        #
        safe_stepsize=jnp.asarray(0.0),
        safe_value=value,
        safe_grad=grad,
    )

  def step_fn(
      state: ZoomLinesearchState,
      *,
      value_and_grad_fn: Callable[
          ..., tuple[jax.typing.ArrayLike, base.Updates]],
      fn_kwargs: dict[str, Any],
  ) -> ZoomLinesearchState:
    """Makes a step of the linesearch."""
    new_state = jax.lax.cond(
        state.interval_found,
        functools.partial(
            _zoom_into_interval,
            value_and_grad_fn=value_and_grad_fn,
            fn_kwargs=fn_kwargs,
        ),
        functools.partial(
            _search_interval,
            value_and_grad_fn=value_and_grad_fn,
            fn_kwargs=fn_kwargs,
        ),
        state,
    )
    new_state = jax.lax.cond(
        new_state.failed, _try_safe_step, lambda x: x, new_state
    )
    return optax.tree.cast_like(new_state, other_tree=state)

  def step_cond_fn(state: ZoomLinesearchState) -> jax.typing.ArrayLike:
    """Continuing criterion for the while loop of the linesearch."""
    return ~(state.done | state.failed)

  return init_fn, step_fn, step_cond_fn

