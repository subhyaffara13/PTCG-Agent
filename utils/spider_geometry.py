
def spider_geometry(const, grad, curv, xpt, xl, xu, delta, debug):
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

    by maximizing the objective function along given straight lines.

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
    xpt : `numpy.ndarray`, shape (n, npt)
        Points defining the straight lines. The straight lines considered are
        the ones passing through the origin and the points in `xpt`.
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
    This function is described as the second alternative in Section 6.5 of
    [1]_. It is assumed that the origin is feasible with respect to the bound
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
        assert (
            isinstance(xpt, np.ndarray)
            and xpt.ndim == 2
            and xpt.shape[0] == grad.size
        )
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

    # Iterate through the straight lines.
    step = np.zeros_like(grad)
    q_val = const
    s_norm = np.linalg.norm(xpt, axis=0)

    # Set alpha_xl to the step size for the lower-bound constraint and
    # alpha_xu to the step size for the upper-bound constraint.

    # xl.shape = (N,)
    # xpt.shape = (N, M)
    # i_xl_pos.shape = (M, N)
    i_xl_pos = (xl > -np.inf) & (xpt.T > -TINY * xl)
    i_xl_neg = (xl > -np.inf) & (xpt.T < TINY * xl)
    i_xu_pos = (xu < np.inf) & (xpt.T > TINY * xu)
    i_xu_neg = (xu < np.inf) & (xpt.T < -TINY * xu)

    # (M, N)
    alpha_xl_pos = np.atleast_2d(
        np.broadcast_to(xl, i_xl_pos.shape)[i_xl_pos] / xpt.T[i_xl_pos]
    )
    # (M,)
    alpha_xl_pos = np.max(alpha_xl_pos, axis=1, initial=-np.inf)
    # make sure it's (M,)
    alpha_xl_pos = np.broadcast_to(np.atleast_1d(alpha_xl_pos), xpt.shape[1])

    alpha_xl_neg = np.atleast_2d(
        np.broadcast_to(xl, i_xl_neg.shape)[i_xl_neg] / xpt.T[i_xl_neg]
    )
    alpha_xl_neg = np.max(alpha_xl_neg, axis=1, initial=np.inf)
    alpha_xl_neg = np.broadcast_to(np.atleast_1d(alpha_xl_neg), xpt.shape[1])

    alpha_xu_neg = np.atleast_2d(
        np.broadcast_to(xu, i_xu_neg.shape)[i_xu_neg] / xpt.T[i_xu_neg]
    )
    alpha_xu_neg = np.max(alpha_xu_neg, axis=1, initial=-np.inf)
    alpha_xu_neg = np.broadcast_to(np.atleast_1d(alpha_xu_neg), xpt.shape[1])

    alpha_xu_pos = np.atleast_2d(
        np.broadcast_to(xu, i_xu_pos.shape)[i_xu_pos] / xpt.T[i_xu_pos]
    )
    alpha_xu_pos = np.max(alpha_xu_pos, axis=1, initial=np.inf)
    alpha_xu_pos = np.broadcast_to(np.atleast_1d(alpha_xu_pos), xpt.shape[1])

    for k in range(xpt.shape[1]):
        # Set alpha_tr to the step size for the trust-region constraint.
        if s_norm[k] > TINY * delta:
            alpha_tr = max(delta / s_norm[k], 0.0)
        else:
            # The current straight line is basically zero.
            continue

        alpha_bd_pos = max(min(alpha_xu_pos[k], alpha_xl_neg[k]), 0.0)
        alpha_bd_neg = min(max(alpha_xl_pos[k], alpha_xu_neg[k]), 0.0)

        # Set alpha_quad_pos and alpha_quad_neg to the step size to the extrema
        # of the quadratic function along the positive and negative directions.
        grad_step = grad @ xpt[:, k]
        curv_step = curv(xpt[:, k])
        if (
            grad_step >= 0.0
            and curv_step < -TINY * grad_step
            or grad_step <= 0.0
            and curv_step > -TINY * grad_step
        ):
            alpha_quad_pos = max(-grad_step / curv_step, 0.0)
        else:
            alpha_quad_pos = np.inf
        if (
            grad_step >= 0.0
            and curv_step > TINY * grad_step
            or grad_step <= 0.0
            and curv_step < TINY * grad_step
        ):
            alpha_quad_neg = min(-grad_step / curv_step, 0.0)
        else:
            alpha_quad_neg = -np.inf

        # Select the step that provides the largest value of the objective
        # function if it improves the current best. The best positive step is
        # either the one that reaches the constraints or the one that reaches
        # the extremum of the objective function along the current direction
        # (only possible if the resulting step is feasible). We test both, and
        # we perform similar calculations along the negative step.
        # N.B.: we select the largest possible step among all the ones that
        # maximize the objective function. This is to avoid returning the zero
        # step in some extreme cases.
        alpha_pos = min(alpha_tr, alpha_bd_pos)
        alpha_neg = max(-alpha_tr, alpha_bd_neg)
        q_val_pos = (
            const + alpha_pos * grad_step + 0.5 * alpha_pos**2.0 * curv_step
        )
        q_val_neg = (
            const + alpha_neg * grad_step + 0.5 * alpha_neg**2.0 * curv_step
        )
        if alpha_quad_pos < alpha_pos:
            q_val_quad_pos = (
                const
                + alpha_quad_pos * grad_step
                + 0.5 * alpha_quad_pos**2.0 * curv_step
            )
            if abs(q_val_quad_pos) > abs(q_val_pos):
                alpha_pos = alpha_quad_pos
                q_val_pos = q_val_quad_pos
        if alpha_quad_neg > alpha_neg:
            q_val_quad_neg = (
                const
                + alpha_quad_neg * grad_step
                + 0.5 * alpha_quad_neg**2.0 * curv_step
            )
            if abs(q_val_quad_neg) > abs(q_val_neg):
                alpha_neg = alpha_quad_neg
                q_val_neg = q_val_quad_neg
        if abs(q_val_pos) >= abs(q_val_neg) and abs(q_val_pos) > abs(q_val):
            step = np.clip(alpha_pos * xpt[:, k], xl, xu)
            q_val = q_val_pos
        elif abs(q_val_neg) > abs(q_val_pos) and abs(q_val_neg) > abs(q_val):
            step = np.clip(alpha_neg * xpt[:, k], xl, xu)
            q_val = q_val_neg

    if debug:
        assert np.all(xl <= step)
        assert np.all(step <= xu)
        assert np.linalg.norm(step) < 1.1 * delta
    return step

