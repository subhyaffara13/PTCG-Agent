from typing import Callable

def jacobian(
    func,
    inputs,
    create_graph=False,
    strict=False,
    vectorize=False,
    strategy="reverse-mode",
):
    r"""Compute the Jacobian of a given function.

    Args:
        func (function): a Python function that takes Tensor inputs and returns
            a tuple of Tensors or a Tensor.
        inputs (tuple of Tensors or Tensor): inputs to the function ``func``.
        create_graph (bool, optional): If ``True``, the Jacobian will be
            computed in a differentiable manner. Note that when ``strict`` is
            ``False``, the result can not require gradients or be disconnected
            from the inputs.  Defaults to ``False``.
        strict (bool, optional): If ``True``, an error will be raised when we
            detect that there exists an input such that all the outputs are
            independent of it. If ``False``, we return a Tensor of zeros as the
            jacobian for said inputs, which is the expected mathematical value.
            Defaults to ``False``.
        vectorize (bool, optional): This feature is experimental.
            Please consider using :func:`torch.func.jacrev` or
            :func:`torch.func.jacfwd` instead if you are looking for something
            less experimental and more performant.
            When computing the jacobian, usually we invoke
            ``autograd.grad`` once per row of the jacobian. If this flag is
            ``True``, we perform only a single ``autograd.grad`` call with
            ``batched_grad=True`` which uses the vmap prototype feature.
            Though this should lead to performance improvements in many cases,
            because this feature is still experimental, there may be performance
            cliffs. See :func:`torch.autograd.grad`'s ``batched_grad`` parameter for
            more information.
        strategy (str, optional): Set to ``"forward-mode"`` or ``"reverse-mode"`` to
            determine whether the Jacobian will be computed with forward or reverse
            mode AD. Currently, ``"forward-mode"`` requires ``vectorized=True``.
            Defaults to ``"reverse-mode"``. If ``func`` has more outputs than
            inputs, ``"forward-mode"`` tends to be more performant. Otherwise,
            prefer to use ``"reverse-mode"``.

    Returns:
        Jacobian (Tensor or nested tuple of Tensors): if there is a single
        input and output, this will be a single Tensor containing the
        Jacobian for the linearized inputs and output. If one of the two is
        a tuple, then the Jacobian will be a tuple of Tensors. If both of
        them are tuples, then the Jacobian will be a tuple of tuple of
        Tensors where ``Jacobian[i][j]`` will contain the Jacobian of the
        ``i``\th output and ``j``\th input and will have as size the
        concatenation of the sizes of the corresponding output and the
        corresponding input and will have same dtype and device as the
        corresponding input. If strategy is ``forward-mode``, the dtype will be
        that of the output; otherwise, the input.

    Example:

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_AUTOGRAD)
        >>> def exp_reducer(x):
        ...     return x.exp().sum(dim=1)
        >>> inputs = torch.rand(2, 2)
        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> jacobian(exp_reducer, inputs)
        tensor([[[1.4917, 2.4352],
                 [0.0000, 0.0000]],
                [[0.0000, 0.0000],
                 [2.4369, 2.3799]]])

        >>> jacobian(exp_reducer, inputs, create_graph=True)
        tensor([[[1.4917, 2.4352],
                 [0.0000, 0.0000]],
                [[0.0000, 0.0000],
                 [2.4369, 2.3799]]], grad_fn=<ViewBackward>)

        >>> def exp_adder(x, y):
        ...     return 2 * x.exp() + 3 * y
        >>> inputs = (torch.rand(2), torch.rand(2))
        >>> jacobian(exp_adder, inputs)
        (tensor([[2.8052, 0.0000],
                [0.0000, 3.3963]]),
         tensor([[3., 0.],
                 [0., 3.]]))

        >>> def linear_model(x):
        ...     W = torch.tensor([[2.0, -1.0], [0.0, 1.0]])
        ...     b = torch.tensor([1.0, 0.5])
        ...     return x @ W.T + b

        >>> x = torch.randn(4, 2, requires_grad=True)
        >>> jac = jacobian(linear_model, x, vectorize=True)
        >>> jac.shape
        torch.Size([4, 2, 4, 2])
    """
    if strategy not in ("forward-mode", "reverse-mode"):
        raise AssertionError(
            'Expected strategy to be either "forward-mode" or "reverse-mode". Hint: If your '
            'function has more outputs than inputs, "forward-mode" tends to be more performant. '
            'Otherwise, prefer to use "reverse-mode".'
        )
    if strategy == "forward-mode":
        if create_graph:
            raise NotImplementedError(
                "torch.autograd.functional.jacobian: `create_graph=True` "
                'and `strategy="forward-mode"` are not supported together (yet). '
                "Please either set `create_graph=False` or "
                '`strategy="reverse-mode"`.'
            )
        return _jacfwd(func, inputs, strict, vectorize)

    with torch.enable_grad():
        is_inputs_tuple, inputs = _as_tuple(inputs, "inputs", "jacobian")
        inputs = _grad_preprocess(inputs, create_graph=create_graph, need_graph=True)

        outputs = func(*inputs)
        is_outputs_tuple, outputs = _as_tuple(
            outputs, "outputs of the user-provided function", "jacobian"
        )
        _check_requires_grad(outputs, "outputs", strict=strict)

        if vectorize:
            if strict:
                raise RuntimeError(
                    "torch.autograd.functional.jacobian: `strict=True` "
                    "and `vectorized=True` are not supported together. "
                    "Please either set `strict=False` or "
                    "`vectorize=False`."
                )
            # NOTE: [Computing jacobian with vmap and grad for multiple outputs]
            #
            # Let's consider f(x) = (x**2, x.sum()) and let x = torch.randn(3).
            # It turns out we can compute the jacobian of this function with a single
            # call to autograd.grad by using vmap over the correct grad_outputs.
            #
            # Firstly, one way to compute the jacobian is to stack x**2 and x.sum()
            # into a 4D vector. E.g., use g(x) = torch.stack([x**2, x.sum()])
            #
            # To get the first row of the jacobian, we call
            # >>> autograd.grad(g(x), x, grad_outputs=torch.tensor([1, 0, 0, 0]))
            # To get the 2nd row of the jacobian, we call
            # >>> autograd.grad(g(x), x, grad_outputs=torch.tensor([0, 1, 0, 0]))
            # and so on.
            #
            # Using vmap, we can vectorize all 4 of these computations into one by
            # passing the standard basis for R^4 as the grad_output.
            # vmap(partial(autograd.grad, g(x), x))(torch.eye(4)).
            #
            # Now, how do we compute the jacobian *without stacking the output*?
            # We can just split the standard basis across the outputs. So to
            # compute the jacobian of f(x), we'd use
            # >>> autograd.grad(f(x), x, grad_outputs=_construct_standard_basis_for(...))
            # The grad_outputs looks like the following:
            # ( torch.tensor([[1, 0, 0],
            #                 [0, 1, 0],
            #                 [0, 0, 1],
            #                 [0, 0, 0]]),
            #   torch.tensor([[0],
            #                 [0],
            #                 [0],
            #                 [1]]) )
            #
            # But we're not done yet!
            # >>> vmap(partial(autograd.grad(f(x), x, grad_outputs=...)))
            # returns a Tensor of shape [4, 3]. We have to remember to split the
            # jacobian of shape [4, 3] into two:
            # - one of shape [3, 3] for the first output
            # - one of shape [   3] for the second output

            # Step 1: Construct grad_outputs by splitting the standard basis
            output_numels = tuple(output.numel() for output in outputs)
            grad_outputs = _construct_standard_basis_for(outputs, output_numels)
            flat_outputs = tuple(output.reshape(-1) for output in outputs)

            # Step 2: Call vmap + autograd.grad
            def vjp(grad_output):
                vj = list(
                    _autograd_grad(
                        flat_outputs,
                        inputs,
                        grad_output,
                        create_graph=create_graph,
                        is_grads_batched=True,
                    )
                )
                for el_idx, vj_el in enumerate(vj):
                    if vj_el is not None:
                        continue
                    vj[el_idx] = torch.zeros_like(inputs[el_idx]).expand(
                        (sum(output_numels),) + inputs[el_idx].shape
                    )
                return tuple(vj)

            jacobians_of_flat_output = vjp(grad_outputs)

            # Step 3: The returned jacobian is one big tensor per input. In this step,
            # we split each Tensor by output.
            jacobian_input_output = []
            for jac_input_i, input_i in zip(jacobians_of_flat_output, inputs):
                jacobian_input_i_output = []
                for jac, output_j in zip(
                    jac_input_i.split(output_numels, dim=0), outputs
                ):
                    jacobian_input_i_output_j = jac.view(output_j.shape + input_i.shape)
                    jacobian_input_i_output.append(jacobian_input_i_output_j)
                jacobian_input_output.append(jacobian_input_i_output)

            # Step 4: Right now, `jacobian` is a List[List[Tensor]].
            # The outer List corresponds to the number of inputs,
            # the inner List corresponds to the number of outputs.
            # We need to exchange the order of these and convert to tuples
            # before returning.
            jacobian_output_input = tuple(zip(*jacobian_input_output))

            jacobian_output_input = _grad_postprocess(
                jacobian_output_input, create_graph
            )
            return _tuple_postprocess(
                jacobian_output_input, (is_outputs_tuple, is_inputs_tuple)
            )

        jacobian: tuple[torch.Tensor, ...] = ()

        for i, out in enumerate(outputs):
            # mypy complains that expression and variable have different types due to the empty list
            jac_i: tuple[list[torch.Tensor]] = tuple([] for _ in range(len(inputs)))  # type: ignore[assignment]
            for j in range(out.nelement()):
                vj = _autograd_grad(
                    (out.reshape(-1)[j],),
                    inputs,
                    retain_graph=True,
                    create_graph=create_graph,
                )

                for el_idx, (jac_i_el, vj_el, inp_el) in enumerate(
                    zip(jac_i, vj, inputs)
                ):
                    if vj_el is not None:
                        if strict and create_graph and not vj_el.requires_grad:
                            msg = (
                                "The jacobian of the user-provided function is "
                                f"independent of input {i}. This is not allowed in "
                                "strict mode when create_graph=True."
                            )
                            raise RuntimeError(msg)
                        jac_i_el.append(vj_el)
                    else:
                        if strict:
                            msg = (
                                f"Output {i} of the user-provided function is "
                                f"independent of input {el_idx}. This is not allowed in "
                                "strict mode."
                            )
                            raise RuntimeError(msg)
                        jac_i_el.append(torch.zeros_like(inp_el))

            # pyrefly: ignore [bad-assignment]
            jacobian += (
                tuple(
                    torch.stack(jac_i_el, dim=0).view(
                        out.size() + inputs[el_idx].size()  # type: ignore[operator]
                    )
                    for (el_idx, jac_i_el) in enumerate(jac_i)
                ),
            )

        jacobian = _grad_postprocess(jacobian, create_graph)

        return _tuple_postprocess(jacobian, (is_outputs_tuple, is_inputs_tuple))


def jacobian(f, x, *, tolerances=None, maxiter=10, order=8, initial_step=0.5,
             step_factor=2.0, step_direction=0):
    r"""Evaluate the Jacobian of a function numerically.

    Parameters
    ----------
    f : callable
        The function whose Jacobian is desired. The signature must be::

            f(xi: ndarray) -> ndarray

        where each element of ``xi`` is a finite real. If the function to be
        differentiated accepts additional arguments, wrap it (e.g. using
        `functools.partial` or ``lambda``) and pass the wrapped callable
        into `jacobian`. `f` must not mutate the array ``xi``. See Notes
        regarding vectorization and the dimensionality of the input and output.
    x : float array_like
        Points at which to evaluate the Jacobian. Must have at least one dimension.
        See Notes regarding the dimensionality and vectorization.
    tolerances : dictionary of floats, optional
        Absolute and relative tolerances. Valid keys of the dictionary are:

        - ``atol`` - absolute tolerance on the derivative
        - ``rtol`` - relative tolerance on the derivative

        Iteration will stop when ``res.error < atol + rtol * abs(res.df)``. The default
        `atol` is the smallest normal number of the appropriate dtype, and
        the default `rtol` is the square root of the precision of the
        appropriate dtype.
    maxiter : int, default: 10
        The maximum number of iterations of the algorithm to perform. See
        Notes.
    order : int, default: 8
        The (positive integer) order of the finite difference formula to be
        used. Odd integers will be rounded up to the next even integer.
    initial_step : float array_like, default: 0.5
        The (absolute) initial step size for the finite difference derivative
        approximation. Must be broadcastable with `x` and `step_direction`.
    step_factor : float, default: 2.0
        The factor by which the step size is *reduced* in each iteration; i.e.
        the step size in iteration 1 is ``initial_step/step_factor``. If
        ``step_factor < 1``, subsequent steps will be greater than the initial
        step; this may be useful if steps smaller than some threshold are
        undesirable (e.g. due to subtractive cancellation error).
    step_direction : int array_like
        An array representing the direction of the finite difference steps (e.g.
        for use when `x` lies near to the boundary of the domain of the function.)
        Must be broadcastable with `x` and `initial_step`.
        Where 0 (default), central differences are used; where negative (e.g.
        -1), steps are non-positive; and where positive (e.g. 1), all steps are
        non-negative.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.

        success : bool array
            ``True`` where the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : The error estimate increased, so iteration was terminated.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.

        df : float array
            The Jacobian of `f` at `x`, if the algorithm terminated
            successfully.
        error : float array
            An estimate of the error: the magnitude of the difference between
            the current estimate of the Jacobian and the estimate in the
            previous iteration.
        nit : int array
            The number of iterations of the algorithm that were performed.
        nfev : int array
            The number of points at which `f` was evaluated.

        Each element of an attribute is associated with the corresponding
        element of `df`. For instance, element ``i`` of `nfev` is the
        number of points at which `f` was evaluated for the sake of
        computing element ``i`` of `df`.

    See Also
    --------
    derivative, hessian

    Notes
    -----
    Suppose we wish to evaluate the Jacobian of a function
    :math:`f: \mathbf{R}^m \rightarrow \mathbf{R}^n`. Assign to variables
    ``m`` and ``n`` the positive integer values of :math:`m` and :math:`n`,
    respectively, and let ``...`` represent an arbitrary tuple of integers.
    If we wish to evaluate the Jacobian at a single point, then:

    - argument `x` must be an array of shape ``(m,)``
    - argument `f` must be vectorized to accept an array of shape ``(m, ...)``.
      The first axis represents the :math:`m` inputs of :math:`f`; the remainder
      are for evaluating the function at multiple points in a single call.
    - argument `f` must return an array of shape ``(n, ...)``. The first
      axis represents the :math:`n` outputs of :math:`f`; the remainder
      are for the result of evaluating the function at multiple points.
    - attribute ``df`` of the result object will be an array of shape ``(n, m)``,
      the Jacobian.

    This function is also vectorized in the sense that the Jacobian can be
    evaluated at ``k`` points in a single call. In this case, `x` would be an
    array of shape ``(m, k)``, `f` would accept an array of shape
    ``(m, k, ...)`` and return an array of shape ``(n, k, ...)``, and the ``df``
    attribute of the result would have shape ``(n, m, k)``.

    Suppose the desired callable ``f_not_vectorized`` is not vectorized; it can
    only accept an array of shape ``(m,)``. A simple solution to satisfy the required
    interface is to wrap ``f_not_vectorized`` as follows::

        def f(x):
            return np.apply_along_axis(f_not_vectorized, axis=0, arr=x)

    Alternatively, suppose the desired callable ``f_vec_q`` is vectorized, but
    only for 2-D arrays of shape ``(m, q)``. To satisfy the required interface,
    consider::

        def f(x):
            m, batch = x.shape[0], x.shape[1:]  # x.shape is (m, ...)
            x = np.reshape(x, (m, -1))  # `-1` is short for q = prod(batch)
            res = f_vec_q(x)  # pass shape (m, q) to function
            n = res.shape[0]
            return np.reshape(res, (n,) + batch)  # return shape (n, ...)

    Then pass the wrapped callable ``f`` as the first argument of `jacobian`.

    References
    ----------
    .. [1] Jacobian matrix and determinant, *Wikipedia*,
           https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant

    Examples
    --------
    The Rosenbrock function maps from :math:`\mathbf{R}^m \rightarrow \mathbf{R}`;
    the SciPy implementation `scipy.optimize.rosen` is vectorized to accept an
    array of shape ``(m, p)`` and return an array of shape ``p``. Suppose we wish
    to evaluate the Jacobian (AKA the gradient because the function returns a scalar)
    at ``[0.5, 0.5, 0.5]``.

    >>> import numpy as np
    >>> from scipy.differentiate import jacobian
    >>> from scipy.optimize import rosen, rosen_der
    >>> m = 3
    >>> x = np.full(m, 0.5)
    >>> res = jacobian(rosen, x)
    >>> ref = rosen_der(x)  # reference value of the gradient
    >>> res.df, ref
    (array([-51.,  -1.,  50.]), array([-51.,  -1.,  50.]))

    As an example of a function with multiple outputs, consider Example 4
    from [1]_.

    >>> def f(x):
    ...     x1, x2, x3 = x
    ...     return [x1, 5*x3, 4*x2**2 - 2*x3, x3*np.sin(x1)]

    The true Jacobian is given by:

    >>> def df(x):
    ...         x1, x2, x3 = x
    ...         one = np.ones_like(x1)
    ...         return [[one, 0*one, 0*one],
    ...                 [0*one, 0*one, 5*one],
    ...                 [0*one, 8*x2, -2*one],
    ...                 [x3*np.cos(x1), 0*one, np.sin(x1)]]

    Evaluate the Jacobian at an arbitrary point.

    >>> rng = np.random.default_rng(389252938452)
    >>> x = rng.random(size=3)
    >>> res = jacobian(f, x)
    >>> ref = df(x)
    >>> res.df.shape == (4, 3)
    True
    >>> np.allclose(res.df, ref)
    True

    Evaluate the Jacobian at 10 arbitrary points in a single call.

    >>> x = rng.random(size=(3, 10))
    >>> res = jacobian(f, x)
    >>> ref = df(x)
    >>> res.df.shape == (4, 3, 10)
    True
    >>> np.allclose(res.df, ref)
    True

    """
    xp = array_namespace(x)
    x0 = xp_promote(x, force_floating=True, xp=xp)

    if x0.ndim < 1:
        message = "Argument `x` must be at least 1-D."
        raise ValueError(message)

    m = x0.shape[0]
    i = xp.arange(m)

    def wrapped(x):
        p = () if x.ndim == x0.ndim else (x.shape[-1],)  # number of abscissae

        new_shape = (m, m) + x0.shape[1:] + p
        xph = xp.expand_dims(x0, axis=1)
        if x.ndim != x0.ndim:
            xph = xp.expand_dims(xph, axis=-1)
        xph = xp_copy(xp.broadcast_to(xph, new_shape), xp=xp)
        xph = xpx.at(xph)[i, i].set(x)
        return f(xph)

    res = derivative(wrapped, x, tolerances=tolerances,
                     maxiter=maxiter, order=order, initial_step=initial_step,
                     step_factor=step_factor, preserve_shape=True,
                     step_direction=step_direction)

    del res.x  # the user knows `x`, and the way it gets broadcasted is meaningless here
    return res


def jacobian(ctx, f, x):
    """
    Calculate the Jacobian matrix of a function at the point x0.

    This is the first derivative of a vectorial function:

        f : R^m -> R^n with m >= n
    """
    x = ctx.matrix(x)
    h = ctx.sqrt(ctx.eps)
    fx = ctx.matrix(f(*x))
    m = len(fx)
    n = len(x)
    J = ctx.matrix(m, n)
    for j in xrange(n):
        xj = x.copy()
        xj[j] += h
        Jj = (ctx.matrix(f(*xj)) - fx) / h
        for i in xrange(m):
            J[i,j] = Jj[i]
    return J


def jacobian(fun: Callable, argnums: int | Sequence[int] = 0,
             has_aux: bool = False, holomorphic: bool = False, allow_int: bool = False) -> Callable:
  """Alias of :func:`jax.jacrev`."""
  return jacrev(fun, argnums=argnums, has_aux=has_aux, holomorphic=holomorphic, allow_int=allow_int)

