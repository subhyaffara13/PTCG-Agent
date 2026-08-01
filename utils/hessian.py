
def hessian(
    func,
    inputs,
    create_graph=False,
    strict=False,
    vectorize=False,
    outer_jacobian_strategy="reverse-mode",
):
    r"""Compute the Hessian of a given scalar function.

    Args:
        func (function): a Python function that takes Tensor inputs and returns
            a Tensor with a single element.
        inputs (tuple of Tensors or Tensor): inputs to the function ``func``.
        create_graph (bool, optional): If ``True``, the Hessian will be computed in
            a differentiable manner. Note that when ``strict`` is ``False``, the result can not
            require gradients or be disconnected from the inputs.
            Defaults to ``False``.
        strict (bool, optional): If ``True``, an error will be raised when we detect that there exists an input
            such that all the outputs are independent of it. If ``False``, we return a Tensor of zeros as the
            hessian for said inputs, which is the expected mathematical value.
            Defaults to ``False``.
        vectorize (bool, optional): This feature is experimental.
            Please consider using :func:`torch.func.hessian`
            instead if you are looking for something less experimental and more performant.
            When computing the hessian, usually we invoke
            ``autograd.grad`` once per row of the hessian. If this flag is
            ``True``, we use the vmap prototype feature as the backend to
            vectorize calls to ``autograd.grad`` so we only invoke it once
            instead of once per row. This should lead to performance
            improvements in many use cases, however, due to this feature
            being incomplete, there may be performance cliffs. Please
            use `torch._C._debug_only_display_vmap_fallback_warnings(True)`
            to show any performance warnings and file us issues if
            warnings exist for your use case. Defaults to ``False``.
        outer_jacobian_strategy (str, optional): The Hessian is computed by
            computing the Jacobian of a Jacobian. The inner Jacobian is always
            computed in reverse-mode AD. Setting strategy to ``"forward-mode"``
            or ``"reverse-mode"`` determines whether the outer Jacobian will be
            computed with forward or reverse mode AD. Currently, computing the outer
            Jacobian in ``"forward-mode"`` requires ``vectorized=True``. Defaults
            to ``"reverse-mode"``.

    Returns:
        Hessian (Tensor or a tuple of tuple of Tensors): if there is a single input,
        this will be a single Tensor containing the Hessian for the input.
        If it is a tuple, then the Hessian will be a tuple of tuples where
        ``Hessian[i][j]`` will contain the Hessian of the ``i``\th input
        and ``j``\th input with size the sum of the size of the ``i``\th input plus
        the size of the ``j``\th input. ``Hessian[i][j]`` will have the same
        dtype and device as the corresponding ``i``\th input.

    Example:

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_AUTOGRAD)
        >>> def pow_reducer(x):
        ...     return x.pow(3).sum()
        >>> inputs = torch.rand(2, 2)
        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> hessian(pow_reducer, inputs)
        tensor([[[[5.2265, 0.0000],
                  [0.0000, 0.0000]],
                 [[0.0000, 4.8221],
                  [0.0000, 0.0000]]],
                [[[0.0000, 0.0000],
                  [1.9456, 0.0000]],
                 [[0.0000, 0.0000],
                  [0.0000, 3.2550]]]])

        >>> hessian(pow_reducer, inputs, create_graph=True)
        tensor([[[[5.2265, 0.0000],
                  [0.0000, 0.0000]],
                 [[0.0000, 4.8221],
                  [0.0000, 0.0000]]],
                [[[0.0000, 0.0000],
                  [1.9456, 0.0000]],
                 [[0.0000, 0.0000],
                  [0.0000, 3.2550]]]], grad_fn=<ViewBackward>)


        >>> def pow_adder_reducer(x, y):
        ...     return (2 * x.pow(2) + 3 * y.pow(2)).sum()
        >>> inputs = (torch.rand(2), torch.rand(2))
        >>> hessian(pow_adder_reducer, inputs)
        ((tensor([[4., 0.],
                  [0., 4.]]),
          tensor([[0., 0.],
                  [0., 0.]])),
         (tensor([[0., 0.],
                  [0., 0.]]),
          tensor([[6., 0.],
                  [0., 6.]])))
    """
    is_inputs_tuple, inputs = _as_tuple(inputs, "inputs", "hessian")
    if outer_jacobian_strategy not in (
        "forward-mode",
        "reverse-mode",
    ):
        raise AssertionError(
            'Expected strategy to be either "forward-mode" or "reverse-mode".'
        )

    def ensure_single_output_function(*inp):
        out = func(*inp)
        is_out_tuple, t_out = _as_tuple(
            out, "outputs of the user-provided function", "hessian"
        )
        _check_requires_grad(t_out, "outputs", strict=strict)

        if is_out_tuple or not isinstance(out, torch.Tensor):
            raise RuntimeError(
                "The function given to hessian should return a single Tensor"
            )

        if out.nelement() != 1:
            raise RuntimeError(
                "The Tensor returned by the function given to hessian should contain a single element"
            )

        return out.squeeze()

    def jac_func(*inp):
        if outer_jacobian_strategy == "forward-mode":
            # _grad_preprocess requires create_graph=True and input to require_grad
            # or else the input will be detached
            inp = tuple(t.requires_grad_(True) for t in inp)
        jac = jacobian(ensure_single_output_function, inp, create_graph=True)
        _check_requires_grad(jac, "jacobian", strict=strict)
        return jac

    res = jacobian(
        jac_func,
        inputs,
        create_graph=create_graph,
        strict=strict,
        vectorize=vectorize,
        strategy=outer_jacobian_strategy,
    )
    return _tuple_postprocess(res, (is_inputs_tuple, is_inputs_tuple))


def hessian(func: Callable[..., Any], argnums: int = 0) -> Callable[..., Any]:
    warn_deprecated("hessian")
    return _impl.hessian(func, argnums=argnums)


def hessian(func: Callable[..., Any], argnums: argnums_t = 0) -> Callable[..., Any]:
    """
    Computes the Hessian of ``func`` with respect to the arg(s) at index
    ``argnum`` via a forward-over-reverse strategy.

    The forward-over-reverse strategy (composing ``jacfwd(jacrev(func))``) is
    a good default for good performance. It is possible to compute Hessians
    through other compositions of :func:`jacfwd` and :func:`jacrev` like
    ``jacfwd(jacfwd(func))`` or ``jacrev(jacrev(func))``.

    Args:
        func (function): A Python function that takes one or more arguments,
            one of which must be a Tensor, and returns one or more Tensors
        argnums (int or tuple[int, ...]): Optional, integer or tuple of integers,
            saying which arguments to get the Hessian with respect to.
            Default: 0.

    Returns:
        Returns a function that takes in the same inputs as ``func`` and
        returns the Hessian of ``func`` with respect to the arg(s) at
        ``argnums``.

    .. note::
        You may see this API error out with "forward-mode AD not implemented
        for operator X". If so, please file a bug report and we will prioritize it.
        An alternative is to use ``jacrev(jacrev(func))``, which has better
        operator coverage.

    A basic usage with a R^N -> R^1 function gives a N x N Hessian:

        >>> from torch.func import hessian
        >>> def f(x):
        >>>   return x.sin().sum()
        >>>
        >>> x = torch.randn(5)
        >>> hess = hessian(f)(x)  # equivalent to jacfwd(jacrev(f))(x)
        >>> assert torch.allclose(hess, torch.diag(-x.sin()))

    """
    return jacfwd(jacrev(func, argnums), argnums)


def hessian(f, varlist, constraints=()):
    """Compute Hessian matrix for a function f wrt parameters in varlist
    which may be given as a sequence or a row/column vector. A list of
    constraints may optionally be given.

    Examples
    ========

    >>> from sympy import Function, hessian, pprint
    >>> from sympy.abc import x, y
    >>> f = Function('f')(x, y)
    >>> g1 = Function('g')(x, y)
    >>> g2 = x**2 + 3*y
    >>> pprint(hessian(f, (x, y), [g1, g2]))
    [                   d               d            ]
    [     0        0    --(g(x, y))     --(g(x, y))  ]
    [                   dx              dy           ]
    [                                                ]
    [     0        0        2*x              3       ]
    [                                                ]
    [                     2               2          ]
    [d                   d               d           ]
    [--(g(x, y))  2*x   ---(f(x, y))   -----(f(x, y))]
    [dx                   2            dy dx         ]
    [                   dx                           ]
    [                                                ]
    [                     2               2          ]
    [d                   d               d           ]
    [--(g(x, y))   3   -----(f(x, y))   ---(f(x, y)) ]
    [dy                dy dx              2          ]
    [                                   dy           ]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Hessian_matrix

    See Also
    ========

    sympy.matrices.matrixbase.MatrixBase.jacobian
    wronskian
    """
    # f is the expression representing a function f, return regular matrix
    if isinstance(varlist, MatrixBase):
        if 1 not in varlist.shape:
            raise ShapeError("`varlist` must be a column or row vector.")
        if varlist.cols == 1:
            varlist = varlist.T
        varlist = varlist.tolist()[0]
    if is_sequence(varlist):
        n = len(varlist)
        if not n:
            raise ShapeError("`len(varlist)` must not be zero.")
    else:
        raise ValueError("Improper variable list in hessian function")
    if not getattr(f, 'diff'):
        # check differentiability
        raise ValueError("Function `f` (%s) is not differentiable" % f)
    m = len(constraints)
    N = m + n
    out = zeros(N)
    for k, g in enumerate(constraints):
        if not getattr(g, 'diff'):
            # check differentiability
            raise ValueError("Function `f` (%s) is not differentiable" % f)
        for i in range(n):
            out[k, i + m] = g.diff(varlist[i])
    for i in range(n):
        for j in range(i, n):
            out[i + m, j + m] = f.diff(varlist[i]).diff(varlist[j])
    for i in range(N):
        for j in range(i + 1, N):
            out[j, i] = out[i, j]
    return out


def hessian(f, x, *, tolerances=None, maxiter=10,
            order=8, initial_step=0.5, step_factor=2.0):
    r"""Evaluate the Hessian of a function numerically.

    Parameters
    ----------
    f : callable
        The function whose Hessian is desired. The signature must be::

            f(xi: ndarray) -> ndarray

        where each element of ``xi`` is a finite real. If the function to be
        differentiated accepts additional arguments, wrap it (e.g. using
        `functools.partial` or ``lambda``) and pass the wrapped callable
        into `hessian`. `f` must not mutate the array ``xi``. See Notes
        regarding vectorization and the dimensionality of the input and output.
    x : float array_like
        Points at which to evaluate the Hessian. Must have at least one dimension.
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
        The maximum number of iterations of the algorithm to perform. See Notes.
    order : int, default: 8
        The (positive integer) order of the finite difference formula to be
        used. Odd integers will be rounded up to the next even integer.
    initial_step : float, default: 0.5
        The (absolute) initial step size for the finite difference derivative
        approximation.
    step_factor : float, default: 2.0
        The factor by which the step size is *reduced* in each iteration; i.e.
        the step size in iteration 1 is ``initial_step/step_factor``. If
        ``step_factor < 1``, subsequent steps will be greater than the initial
        step; this may be useful if steps smaller than some threshold are
        undesirable (e.g. due to subtractive cancellation error).

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

        ddf : float array
            The Hessian of `f` at `x`, if the algorithm terminated
            successfully.
        error : float array
            An estimate of the error: the magnitude of the difference between
            the current estimate of the Hessian and the estimate in the
            previous iteration.
        nfev : int array
            The number of points at which `f` was evaluated.

        Each element of an attribute is associated with the corresponding
        element of `ddf`. For instance, element ``[i, j]`` of `nfev` is the
        number of points at which `f` was evaluated for the sake of
        computing element ``[i, j]`` of `ddf`.

    See Also
    --------
    derivative, jacobian

    Notes
    -----
    Suppose we wish to evaluate the Hessian of a function
    :math:`f: \mathbf{R}^m \rightarrow \mathbf{R}`, and we assign to variable
    ``m`` the positive integer value of :math:`m`. If we wish to evaluate
    the Hessian at a single point, then:

    - argument `x` must be an array of shape ``(m,)``
    - argument `f` must be vectorized to accept an array of shape
      ``(m, ...)``. The first axis represents the :math:`m` inputs of
      :math:`f`; the remaining axes indicated by ellipses are for evaluating
      the function at several abscissae in a single call.
    - argument `f` must return an array of shape ``(...)``.
    - attribute ``dff`` of the result object will be an array of shape ``(m, m)``,
      the Hessian.

    This function is also vectorized in the sense that the Hessian can be
    evaluated at ``k`` points in a single call. In this case, `x` would be an
    array of shape ``(m, k)``, `f` would accept an array of shape
    ``(m, ...)`` and return an array of shape ``(...)``, and the ``ddf``
    attribute of the result would have shape ``(m, m, k)``. Note that the
    axis associated with the ``k`` points is included within the axes
    denoted by ``(...)``.

    Currently, `hessian` is implemented by nesting calls to `jacobian`.
    All options passed to `hessian` are used for both the inner and outer
    calls with one exception: the `rtol` used in the inner `jacobian` call
    is tightened by a factor of 100 with the expectation that the inner
    error can be ignored. A consequence is that `rtol` should not be set
    less than 100 times the precision of the dtype of `x`; a warning is
    emitted otherwise.

    References
    ----------
    .. [1] Hessian matrix, *Wikipedia*,
           https://en.wikipedia.org/wiki/Hessian_matrix

    Examples
    --------
    The Rosenbrock function maps from :math:`\mathbf{R}^m \rightarrow \mathbf{R}`;
    the SciPy implementation `scipy.optimize.rosen` is vectorized to accept an
    array of shape ``(m, ...)`` and return an array of shape ``...``. Suppose we
    wish to evaluate the Hessian at ``[0.5, 0.5, 0.5]``.

    >>> import numpy as np
    >>> from scipy.differentiate import hessian
    >>> from scipy.optimize import rosen, rosen_hess
    >>> m = 3
    >>> x = np.full(m, 0.5)
    >>> res = hessian(rosen, x)
    >>> ref = rosen_hess(x)  # reference value of the Hessian
    >>> np.allclose(res.ddf, ref)
    True

    `hessian` is vectorized to evaluate the Hessian at multiple points
    in a single call.

    >>> rng = np.random.default_rng(4589245925010)
    >>> x = rng.random((m, 10))
    >>> res = hessian(rosen, x)
    >>> ref = [rosen_hess(xi) for xi in x.T]
    >>> ref = np.moveaxis(ref, 0, -1)
    >>> np.allclose(res.ddf, ref)
    True

    """
    # todo:
    # - add ability to vectorize over additional parameters (*args?)
    # - error estimate stack with inner jacobian (or use legit 2D stencil)

    kwargs = dict(maxiter=maxiter, order=order, initial_step=initial_step,
                  step_factor=step_factor)
    tolerances = {} if tolerances is None else tolerances
    atol = tolerances.get('atol', None)
    rtol = tolerances.get('rtol', None)

    xp = array_namespace(x)
    x0 = xp_promote(x, force_floating=True, xp=xp)

    finfo = xp.finfo(x0.dtype)
    rtol = finfo.eps**0.5 if rtol is None else rtol  # keep same as `derivative`

    # tighten the inner tolerance to make the inner error negligible
    rtol_min = finfo.eps * 100
    message = (f"The specified `{rtol=}`, but error estimates are likely to be "
               f"unreliable when `rtol < {rtol_min}`.")
    if 0 < rtol < rtol_min:  # rtol <= 0 is an error
        warnings.warn(message, RuntimeWarning, stacklevel=2)
        rtol = rtol_min

    def df(x):
        tolerances = dict(rtol=rtol/100, atol=atol)
        temp = jacobian(f, x, tolerances=tolerances, **kwargs)
        nfev.append(temp.nfev if len(nfev) == 0 else temp.nfev.sum(axis=-1))
        return temp.df

    nfev = []  # track inner function evaluations
    res = jacobian(df, x, tolerances=tolerances, **kwargs)  # jacobian of jacobian

    nfev = xp.cumulative_sum(xp.stack(nfev), axis=0)
    res_nit = xp.astype(res.nit[xp.newaxis, ...], xp.int64)  # appease torch
    res.nfev = xp.take_along_axis(nfev, res_nit, axis=0)[0]
    res.ddf = res.df
    del res.df  # this is renamed to ddf
    del res.nit  # this is only the outer-jacobian nit

    return res


def hessian(fun: Callable, argnums: int | Sequence[int] = 0,
            has_aux: bool = False, holomorphic: bool = False) -> Callable:
  """Hessian of ``fun`` as a dense array.

  Args:
    fun: Function whose Hessian is to be computed.  Its arguments at positions
      specified by ``argnums`` should be arrays, scalars, or standard Python
      containers thereof. It should return arrays, scalars, or standard Python
      containers thereof.
    argnums: Optional, integer or sequence of integers. Specifies which
      positional argument(s) to differentiate with respect to (default ``0``).
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the
      first element is considered the output of the mathematical function to be
      differentiated and the second element is auxiliary data. Default False.
    holomorphic: Optional, bool. Indicates whether ``fun`` is promised to be
      holomorphic. Default False.

  Returns:
    A function with the same arguments as ``fun``, that evaluates the Hessian of
    ``fun``.

  >>> import jax
  >>>
  >>> g = lambda x: x[0]**3 - 2*x[0]*x[1] - x[1]**6
  >>> print(jax.hessian(g)(jax.numpy.array([1., 2.])))
  [[   6.   -2.]
   [  -2. -480.]]

  :py:func:`hessian` is a generalization of the usual definition of the Hessian
  that supports nested Python containers (i.e. pytrees) as inputs and outputs.
  The tree structure of ``jax.hessian(fun)(x)`` is given by forming a tree
  product of the structure of ``fun(x)`` with a tree product of two copies of
  the structure of ``x``. A tree product of two tree structures is formed by
  replacing each leaf of the first tree with a copy of the second. For example:

  >>> import jax.numpy as jnp
  >>> f = lambda dct: {"c": jnp.power(dct["a"], dct["b"])}
  >>> print(jax.hessian(f)({"a": jnp.arange(2.) + 1., "b": jnp.arange(2.) + 2.}))
  {'c': {'a': {'a': Array([[[ 2.,  0.], [ 0.,  0.]],
                           [[ 0.,  0.], [ 0., 12.]]], dtype=float32),
               'b': Array([[[ 1.      ,  0.      ], [ 0.      ,  0.      ]],
                           [[ 0.      ,  0.      ], [ 0.      , 12.317766]]], dtype=float32)},
         'b': {'a': Array([[[ 1.      ,  0.      ], [ 0.      ,  0.      ]],
                           [[ 0.      ,  0.      ], [ 0.      , 12.317766]]], dtype=float32),
               'b': Array([[[0.      , 0.      ], [0.      , 0.      ]],
                           [[0.      , 0.      ], [0.      , 3.843624]]], dtype=float32)}}}

  Thus each leaf in the tree structure of ``jax.hessian(fun)(x)`` corresponds to
  a leaf of ``fun(x)`` and a pair of leaves of ``x``. For each leaf in
  ``jax.hessian(fun)(x)``, if the corresponding array leaf of ``fun(x)`` has
  shape ``(out_1, out_2, ...)`` and the corresponding array leaves of ``x`` have
  shape ``(in_1_1, in_1_2, ...)`` and ``(in_2_1, in_2_2, ...)`` respectively,
  then the Hessian leaf has shape ``(out_1, out_2, ..., in_1_1, in_1_2, ...,
  in_2_1, in_2_2, ...)``. In other words, the Python tree structure represents
  the block structure of the Hessian, with blocks determined by the input and
  output pytrees.

  In particular, an array is produced (with no pytrees involved) when the
  function input ``x`` and output ``fun(x)`` are each a single array, as in the
  ``g`` example above. If ``fun(x)`` has shape ``(out1, out2, ...)`` and ``x``
  has shape ``(in1, in2, ...)`` then ``jax.hessian(fun)(x)`` has shape
  ``(out1, out2, ..., in1, in2, ..., in1, in2, ...)``. To flatten pytrees into
  1D vectors, consider using :py:func:`jax.flatten_util.flatten_pytree`.
  """
  return jacfwd(jacrev(fun, argnums, has_aux=has_aux, holomorphic=holomorphic),
                argnums, has_aux=has_aux, holomorphic=holomorphic)

