
def bisect(shape_env):
    from torch.fx.experimental.recording import (
        FakeTensorMeta,
        replay_shape_env_events,
        ShapeEnvEvent,
    )
    from torch.fx.experimental.symbolic_shapes import (
        CURRENT_NODE_KEY,
        ShapeEnv,
        SHAPEENV_EVENT_KEY,
    )

    events = shape_env.events

    # Retrieves the ShapeEnvEvent associated with node.
    def get_node_event(node: torch.fx.Node) -> ShapeEnvEvent:
        if SHAPEENV_EVENT_KEY not in node.meta:
            raise AssertionError("SHAPEENV_EVENT_KEY not in node.meta")
        return events[node.meta[SHAPEENV_EVENT_KEY]]

    # Creates a new instance of fake, but updating every symbolic value's ShapeEnv
    # reference to the one given as argument.
    #
    # This is needed so as not to simplify a symbolic expression using a ShapeEnv
    # "from the future", where it may have a different set of replacements.
    def new_with_shape_env(shape_env: ShapeEnv, fake) -> Any:
        if isinstance(fake, int):
            return fake
        if isinstance(fake, torch.SymInt):
            return torch.SymInt(fake.node.with_shape_env(shape_env))
        if isinstance(fake, torch.SymFloat):
            return torch.SymFloat(fake.node.with_shape_env(shape_env))
        if not isinstance(fake, FakeTensorMeta):
            raise AssertionError(f"Expected FakeTensorMeta, got {type(fake)}")
        return FakeTensorMeta(
            tuple(new_with_shape_env(shape_env, s) for s in fake.size()),
            tuple(new_with_shape_env(shape_env, s) for s in fake.stride()),
            new_with_shape_env(shape_env, fake.storage_offset()),
            fake.is_nested,
        )

    # Checks whether the given shape_env fails when produce_guards is called.
    def check_shapeenv_fails(
        shape_env: ShapeEnv, tracked_fakes: list[Any] | None
    ) -> ValidationException | None:
        if tracked_fakes is None:
            raise AssertionError("tracked_fakes is None")
        try:
            # This produce_guards call is a best-effort replication, since we
            # don't populate EqualityConstraint list. Reason: we would also have
            # to save OutputGraph.tracked_fakes_id_to_source.
            shape_env.produce_guards(
                [new_with_shape_env(shape_env, a.fake) for a in tracked_fakes],
                [a.source for a in tracked_fakes],
                input_contexts=[a.symbolic_context for a in tracked_fakes],
            )
            return None
        except ValidationException as e:
            return e

    # Checks whether the ShapeEnv reconstructed by replaying the events until
    # node is created fails when produce_guards is called.
    def check_node_fails(node: torch.fx.Node) -> ValidationException | None:
        number = node.meta[SHAPEENV_EVENT_KEY]
        # Reconstruct shape_env until the event at event_number.
        shape_env = replay_shape_env_events(events[: number + 1])
        shape_env.graph.lint()
        return check_shapeenv_fails(shape_env, events[number].tracked_fakes)

    last_exception = check_shapeenv_fails(
        shape_env, shape_env._snapshot_tracked_fakes()
    )

    if not last_exception:
        # We don't actually fail due to a produce_guards call.
        # Stop and don't bisect.
        log.info("translation validation succeeded: no errors found.")
        return

    if not shape_env.should_record_events or config.translation_validation_no_bisect:
        # Bisection is off.
        # Return the last ValidationException we got.
        raise last_exception

    # Cache the raised exception (if any) at each bisection point.
    exception = {}

    # Bisection happens on the assertion nodes of the recorded FX graph for
    # dynamic shapes.
    assert_nodes = [
        node for node in shape_env.graph.nodes if node.target is torch._assert
    ]

    # Preparing the indices for binary search.
    # The overall invariants are
    # - for all i < left, assert_node[i] doesn't fail
    # - for all i >= right, assert_node[i] fails
    # - `right in exception` always holds
    # - `left <= right` always holds
    left, mid, right = 0, 0, len(assert_nodes) - 1
    exception[right] = check_node_fails(assert_nodes[right])

    while left < right:
        mid = (left + right) // 2

        node = assert_nodes[mid]
        log.debug("bisecting at %s: %s", mid, get_node_event(node))

        # Check whether the new shape_env raises a ValidationException or not.
        exception[mid] = check_node_fails(node)

        if exception[mid]:
            right = mid
        else:
            left = mid + 1

    if not (left in exception and isinstance(exception[left], ValidationException)):
        raise AssertionError("Expected ValidationException at bisect result")

    node = assert_nodes[left]
    event = get_node_event(node)

    if event.is_evaluate_expr():
        failed_action = "evaluating"
    else:
        if not event.is_defer_runtime_assert():
            raise AssertionError(f"unexpected event type: {event}")
        failed_action = "adding runtime assert"

    args = event.args
    if args is None:
        raise AssertionError("event.args is None")
    if len(args) < 2:
        raise AssertionError(
            f"bisecting expects {event.name} to have at least 2 positional arguments. "
            f"Got: {len(args)}"
        )
    if not isinstance(args[1], sympy.Basic):
        raise AssertionError(
            f"bisecting expects {event.name} to have a SymPy expression as its second "
            f"argument. Got: {type(args[1])}"
        )

    raise BisectValidationException(
        exception[left],
        expr=args[1],
        failed_action=failed_action,
        traced_node=node.meta[CURRENT_NODE_KEY],
    )


def bisect(f, a, b, args=(),
           xtol=_xtol, rtol=_rtol, maxiter=_iter,
           full_output=False, disp=True):
    """
    Find root of a function within an interval using bisection.

    Basic bisection routine to find a root of the function `f` between the
    arguments `a` and `b`. ``f(a)`` and ``f(b)`` cannot have the same signs.
    Slow but sure.

    Parameters
    ----------
    f : function
        Python function returning a number.  `f` must be continuous, and
        ``f(a)`` and ``f(b)`` must have opposite signs.
    a : scalar
        One end of the bracketing interval ``[a,b]``.
    b : scalar
        The other end of the bracketing interval ``[a,b]``.
    args : tuple, optional
        Containing extra arguments for the function `f`.
        `f` is called by ``apply(f, (x)+args)``.
    xtol : number, optional
        The computed root ``x0`` will satisfy ``np.isclose(x, x0,
        atol=xtol, rtol=rtol)``, where ``x`` is the exact root. The
        parameter must be positive.
    rtol : number, optional
        The computed root ``x0`` will satisfy ``np.isclose(x, x0,
        atol=xtol, rtol=rtol)``, where ``x`` is the exact root. The
        parameter cannot be smaller than its default value of
        ``4*np.finfo(float).eps``.
    maxiter : int, optional
        If convergence is not achieved in `maxiter` iterations, an error is
        raised. Must be >= 0.
    full_output : bool, optional
        If `full_output` is False, the root is returned. If `full_output` is
        True, the return value is ``(x, r)``, where x is the root, and r is
        a `RootResults` object.
    disp : bool, optional
        If True, raise RuntimeError if the algorithm didn't converge.
        Otherwise, the convergence status is recorded in a `RootResults`
        return object.

    Returns
    -------
    root : float
        Root of `f` between `a` and `b`.
    r : `RootResults` (present if ``full_output = True``)
        Object containing information about the convergence. In particular,
        ``r.converged`` is True if the routine converged.

    See Also
    --------
    brentq, brenth, bisect, newton
    fixed_point : scalar fixed-point finder
    fsolve : n-dimensional root-finding
    elementwise.find_root : efficient elementwise 1-D root-finder

    Notes
    -----
    As mentioned in the parameter documentation, the computed root ``x0`` will
    satisfy ``np.isclose(x, x0, atol=xtol, rtol=rtol)``, where ``x`` is the
    exact root. In equation form, this terminating condition is ``abs(x - x0)
    <= xtol + rtol * abs(x0)``.

    The default value ``xtol=2e-12`` may lead to surprising behavior if one
    expects `bisect` to always compute roots with relative error near machine
    precision. Care should be taken to select `xtol` for the use case at hand.
    Setting ``xtol=5e-324``, the smallest subnormal number, will ensure the
    highest level of accuracy. Larger values of `xtol` may be useful for saving
    function evaluations when a root is at or near zero in applications where
    the tiny absolute differences available between floating point numbers near
    zero are not meaningful.

    Examples
    --------

    >>> def f(x):
    ...     return (x**2 - 1)

    >>> from scipy import optimize

    >>> root = optimize.bisect(f, 0, 2)
    >>> root
    1.0

    >>> root = optimize.bisect(f, -2, 0)
    >>> root
    -1.0
    """
    if not isinstance(args, tuple):
        args = (args,)
    maxiter = operator.index(maxiter)
    if xtol <= 0:
        raise ValueError(f"xtol too small ({xtol:g} <= 0)")
    if rtol < _rtol:
        raise ValueError(f"rtol too small ({rtol:g} < {_rtol:g})")
    f = _wrap_nan_raise(f)
    r = _zeros._bisect(f, a, b, xtol, rtol, maxiter, args, full_output, disp)
    return results_c(full_output, r, "bisect")

