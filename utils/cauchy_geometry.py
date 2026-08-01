
def cauchy_geometry(const, grad, curv, xl, xu, delta, debug):
    r"""
    Maximize approximately the absolute value of a quadratic function subject
    to bound constraints in a trust region.

    This function solves approximately

    .. math::

        \max_{s \in \mathbb{R}^n} \quad \bigg\lvert c + g^{\mathsf{T}} s +
        \frac{1}{2} s^{\mathsf{T}} H s \bigg\rvert \quad \text{s.t.} \quad
        \left\{ \begin{array}{l}
            l \le s \le u,\\
            \lVert s \rVert \le \Delta,
        \end{array} \right.

    by maximizing the objective function along the constrained Cauchy
    direction.

    Parameters
    ----------
    const : float
        Constant :math:`c` as shown above.
    grad : `numpy.ndarray`, shape (n,)
        Gradient :math:`g` as shown above.
    curv : callable
        Curvature of :math:`H` along any vector.

            ``curv(s) -> float``

        returns :math:`s^{\mathsf{T}} H s`.
    xl : `numpy.ndarray`, shape (n,)
        Lower bounds :math:`l` as shown above.
    xu : `numpy.ndarray`, shape (n,)
        Upper bounds :math:`u` as shown above.
    delta : float
        Trust-region radius :math:`\Delta` as shown above.
    debug : bool
        Whether to make debugging tests during the execution.

    Returns
    -------
    `numpy.ndarray`, shape (n,)
        Approximate solution :math:`s`.

    Notes
    -----
    This function is described as the first alternative in Section 6.5 of [1]_.
    It is assumed that the origin is feasible with respect to the bound
    constraints and that `delta` is finite and positive.

    References
    ----------
    .. [1] T. M. Ragonneau. *Model-Based Derivative-Free Optimization Methods
       and Software*. PhD thesis, Department of Applied Mathematics, The Hong
       Kong Polytechnic University, Hong Kong, China, 2022. URL:
       https://theses.lib.polyu.edu.hk/handle/200/12294.
    """
    if debug:
        assert isinstance(const, float)
        assert isinstance(grad, np.ndarray) and grad.ndim == 1
        assert inspect.signature(curv).bind(grad)
        assert isinstance(xl, np.ndarray) and xl.shape == grad.shape
        assert isinstance(xu, np.ndarray) and xu.shape == grad.shape
        assert isinstance(delta, float)
        assert isinstance(debug, bool)
        tol = get_arrays_tol(xl, xu)
        assert np.all(xl <= tol)
        assert np.all(xu >= -tol)
        assert np.isfinite(delta) and delta > 0.0
    xl = np.minimum(xl, 0.0)
    xu = np.maximum(xu, 0.0)

    # To maximize the absolute value of a quadratic function, we maximize the
    # function itself or its negative, and we choose the solution that provides
    # the largest function value.
    step1, q_val1 = _cauchy_geom(const, grad, curv, xl, xu, delta, debug)
    step2, q_val2 = _cauchy_geom(
        -const,
        -grad,
        lambda x: -curv(x),
        xl,
        xu,
        delta,
        debug,
    )
    step = step1 if abs(q_val1) >= abs(q_val2) else step2

    if debug:
        assert np.all(xl <= step)
        assert np.all(step <= xu)
        assert np.linalg.norm(step) < 1.1 * delta
    return step

