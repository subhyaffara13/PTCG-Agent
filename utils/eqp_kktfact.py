
def eqp_kktfact(H, c, A, b):
    """Solve equality-constrained quadratic programming (EQP) problem.

    Solve ``min 1/2 x.T H x + x.t c`` subject to ``A x + b = 0``
    using direct factorization of the KKT system.

    Parameters
    ----------
    H : sparse array, shape (n, n)
        Hessian matrix of the EQP problem.
    c : array_like, shape (n,)
        Gradient of the quadratic objective function.
    A : sparse array
        Jacobian matrix of the EQP problem.
    b : array_like, shape (m,)
        Right-hand side of the constraint equation.

    Returns
    -------
    x : array_like, shape (n,)
        Solution of the KKT problem.
    lagrange_multipliers : ndarray, shape (m,)
        Lagrange multipliers of the KKT problem.
    """
    n, = np.shape(c)  # Number of parameters
    m, = np.shape(b)  # Number of constraints

    # Karush-Kuhn-Tucker matrix of coefficients.
    # Defined as in Nocedal/Wright "Numerical
    # Optimization" p.452 in Eq. (16.4).
    kkt_matrix = block_array([[H, A.T], [A, None]], format="csc")
    # Vector of coefficients.
    kkt_vec = np.hstack([-c, -b])

    # TODO: Use a symmetric indefinite factorization
    #       to solve the system twice as fast (because
    #       of the symmetry).
    lu = linalg.splu(kkt_matrix)
    kkt_sol = lu.solve(kkt_vec)
    x = kkt_sol[:n]
    lagrange_multipliers = -kkt_sol[n:n+m]

    return x, lagrange_multipliers

