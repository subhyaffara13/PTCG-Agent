
def modified_dogleg(A, Y, b, trust_radius, lb, ub):
    """Approximately  minimize ``1/2*|| A x + b ||^2`` inside trust-region.

    Approximately solve the problem of minimizing ``1/2*|| A x + b ||^2``
    subject to ``||x|| < Delta`` and ``lb <= x <= ub`` using a modification
    of the classical dogleg approach.

    Parameters
    ----------
    A : LinearOperator (or sparse array or ndarray), shape (m, n)
        Matrix ``A`` in the minimization problem. It should have
        dimension ``(m, n)`` such that ``m < n``.
    Y : LinearOperator (or sparse array or ndarray), shape (n, m)
        LinearOperator that apply the projection matrix
        ``Q = A.T inv(A A.T)`` to the vector. The obtained vector
        ``y = Q x`` being the minimum norm solution of ``A y = x``.
    b : array_like, shape (m,)
        Vector ``b``in the minimization problem.
    trust_radius: float
        Trust radius to be considered. Delimits a sphere boundary
        to the problem.
    lb : array_like, shape (n,)
        Lower bounds to each one of the components of ``x``.
        It is expected that ``lb <= 0``, otherwise the algorithm
        may fail. If ``lb[i] = -Inf``, the lower
        bound for the ith component is just ignored.
    ub : array_like, shape (n, )
        Upper bounds to each one of the components of ``x``.
        It is expected that ``ub >= 0``, otherwise the algorithm
        may fail. If ``ub[i] = Inf``, the upper bound for the ith
        component is just ignored.

    Returns
    -------
    x : array_like, shape (n,)
        Solution to the problem.

    Notes
    -----
    Based on implementations described in pp. 885-886 from [1]_.

    References
    ----------
    .. [1] Byrd, Richard H., Mary E. Hribar, and Jorge Nocedal.
           "An interior point algorithm for large-scale nonlinear
           programming." SIAM Journal on Optimization 9.4 (1999): 877-900.
    """
    # Compute minimum norm minimizer of 1/2*|| A x + b ||^2.
    newton_point = -Y.dot(b)
    # Check for interior point
    if inside_box_boundaries(newton_point, lb, ub)  \
       and norm(newton_point) <= trust_radius:
        x = newton_point
        return x

    # Compute gradient vector ``g = A.T b``
    g = A.T.dot(b)
    # Compute Cauchy point
    # `cauchy_point = g.T g / (g.T A.T A g)``.
    A_g = A.dot(g)
    cauchy_point = -np.dot(g, g) / np.dot(A_g, A_g) * g
    # Origin
    origin_point = np.zeros_like(cauchy_point)

    # Check the segment between cauchy_point and newton_point
    # for a possible solution.
    z = cauchy_point
    p = newton_point - cauchy_point
    _, alpha, intersect = box_sphere_intersections(z, p, lb, ub,
                                                   trust_radius)
    if intersect:
        x1 = z + alpha*p
    else:
        # Check the segment between the origin and cauchy_point
        # for a possible solution.
        z = origin_point
        p = cauchy_point
        _, alpha, _ = box_sphere_intersections(z, p, lb, ub,
                                               trust_radius)
        x1 = z + alpha*p

    # Check the segment between origin and newton_point
    # for a possible solution.
    z = origin_point
    p = newton_point
    _, alpha, _ = box_sphere_intersections(z, p, lb, ub,
                                           trust_radius)
    x2 = z + alpha*p

    # Return the best solution among x1 and x2.
    if norm(A.dot(x1) + b) < norm(A.dot(x2) + b):
        return x1
    else:
        return x2

