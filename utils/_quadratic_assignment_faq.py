
def _quadratic_assignment_faq(A, B,
                              maximize=False, partial_match=None, rng=None,
                              P0="barycenter", shuffle_input=False, maxiter=30,
                              tol=0.03, **unknown_options):
    r"""Solve the quadratic assignment problem (approximately).

    This function solves the Quadratic Assignment Problem (QAP) and the
    Graph Matching Problem (GMP) using the Fast Approximate QAP Algorithm
    (FAQ) [1]_.

    Quadratic assignment solves problems of the following form:

    .. math::

        \min_P & \ {\ \text{trace}(A^T P B P^T)}\\
        \mbox{s.t. } & {P \ \epsilon \ \mathcal{P}}\\

    where :math:`\mathcal{P}` is the set of all permutation matrices,
    and :math:`A` and :math:`B` are square matrices.

    Graph matching tries to *maximize* the same objective function.
    This algorithm can be thought of as finding the alignment of the
    nodes of two graphs that minimizes the number of induced edge
    disagreements, or, in the case of weighted graphs, the sum of squared
    edge weight differences.

    Note that the quadratic assignment problem is NP-hard. The results given
    here are approximations and are not guaranteed to be optimal.

    Parameters
    ----------
    A : 2-D array, square
        The square matrix :math:`A` in the objective function above.
    B : 2-D array, square
        The square matrix :math:`B` in the objective function above.
    method :  str in {'faq', '2opt'} (default: 'faq')
        The algorithm used to solve the problem. This is the method-specific
        documentation for 'faq'.
        :ref:`'2opt' <optimize.qap-2opt>` is also available.

    Options
    -------
    maximize : bool (default: False)
        Maximizes the objective function if ``True``.
    partial_match : 2-D array of integers, optional (default: None)
        Fixes part of the matching. Also known as a "seed" [2]_.

        Each row of `partial_match` specifies a pair of matched nodes:
        node ``partial_match[i, 0]`` of `A` is matched to node
        ``partial_match[i, 1]`` of `B`. The array has shape ``(m, 2)``, where
        ``m`` is not greater than the number of nodes, :math:`n`.

    rng : {None, int, `numpy.random.Generator`}, optional
        Pseudorandom number generator state. See `quadratic_assignment` for details.
    P0 : 2-D array, "barycenter", or "randomized" (default: "barycenter")
        Initial position. Must be a doubly-stochastic matrix [3]_.

        If the initial position is an array, it must be a doubly stochastic
        matrix of size :math:`m' \times m'` where :math:`m' = n - m`.

        If ``"barycenter"`` (default), the initial position is the barycenter
        of the Birkhoff polytope (the space of doubly stochastic matrices).
        This is a :math:`m' \times m'` matrix with all entries equal to
        :math:`1 / m'`.

        If ``"randomized"`` the initial search position is
        :math:`P_0 = (J + K) / 2`, where :math:`J` is the barycenter and
        :math:`K` is a random doubly stochastic matrix.
    shuffle_input : bool (default: False)
        Set to `True` to resolve degenerate gradients randomly. For
        non-degenerate gradients this option has no effect.
    maxiter : int, positive (default: 30)
        Integer specifying the max number of Frank-Wolfe iterations performed.
    tol : float (default: 0.03)
        Tolerance for termination. Frank-Wolfe iteration terminates when
        :math:`\frac{||P_{i}-P_{i+1}||_F}{\sqrt{m'}} \leq tol`,
        where :math:`i` is the iteration number.

    Returns
    -------
    res : OptimizeResult
        `OptimizeResult` containing the following fields.

        col_ind : 1-D array
            Column indices corresponding to the best permutation found of the
            nodes of `B`.
        fun : float
            The objective value of the solution.
        nit : int
            The number of Frank-Wolfe iterations performed.

    Notes
    -----
    The algorithm may be sensitive to the initial permutation matrix (or
    search "position") due to the possibility of several local minima
    within the feasible region. A barycenter initialization is more likely to
    result in a better solution than a single random initialization. However,
    calling ``quadratic_assignment`` several times with different random
    initializations may result in a better optimum at the cost of longer
    total execution time.

    Examples
    --------
    As mentioned above, a barycenter initialization often results in a better
    solution than a single random initialization.

    >>> from scipy.optimize import quadratic_assignment
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> n = 15
    >>> A = rng.random((n, n))
    >>> B = rng.random((n, n))
    >>> options = {"rng": rng}
    >>> res = quadratic_assignment(A, B, options=options)  # FAQ is default method
    >>> print(res.fun)
    47.797048706380636  # may vary

    >>> options = {"rng": rng, "P0": "randomized"}  # use randomized initialization
    >>> res = quadratic_assignment(A, B, options=options)
    >>> print(res.fun)
    47.37287069769966 # may vary

    However, consider running from several randomized initializations and
    keeping the best result.

    >>> res = min([quadratic_assignment(A, B, options=options)
    ...            for i in range(30)], key=lambda x: x.fun)
    >>> print(res.fun)
    46.55974835248574 # may vary

    The '2-opt' method can be used to attempt to refine the results.

    >>> options = {"partial_guess": np.array([np.arange(n), res.col_ind]).T, "rng": rng}
    >>> res = quadratic_assignment(A, B, method="2opt", options=options)
    >>> print(res.fun)
    46.55974835248574 # may vary

    References
    ----------
    .. [1] J.T. Vogelstein, J.M. Conroy, V. Lyzinski, L.J. Podrazik,
           S.G. Kratzer, E.T. Harley, D.E. Fishkind, R.J. Vogelstein, and
           C.E. Priebe, "Fast approximate quadratic programming for graph
           matching," PLOS one, vol. 10, no. 4, p. e0121002, 2015,
           :doi:`10.1371/journal.pone.0121002`

    .. [2] D. Fishkind, S. Adali, H. Patsolic, L. Meng, D. Singh, V. Lyzinski,
           C. Priebe, "Seeded graph matching", Pattern Recognit. 87 (2019):
           203-215, :doi:`10.1016/j.patcog.2018.09.014`

    .. [3] "Doubly stochastic Matrix," Wikipedia.
           https://en.wikipedia.org/wiki/Doubly_stochastic_matrix

    """

    _check_unknown_options(unknown_options)

    maxiter = operator.index(maxiter)

    # ValueError check
    A, B, partial_match = _common_input_validation(A, B, partial_match)

    msg = None
    if isinstance(P0, str) and P0 not in {'barycenter', 'randomized'}:
        msg = "Invalid 'P0' parameter string"
    elif maxiter <= 0:
        msg = "'maxiter' must be a positive integer"
    elif tol <= 0:
        msg = "'tol' must be a positive float"
    if msg is not None:
        raise ValueError(msg)

    rng = np.random.default_rng(rng)
    n = len(A)  # number of vertices in graphs
    n_seeds = len(partial_match)  # number of seeds
    n_unseed = n - n_seeds

    # [1] Algorithm 1 Line 1 - choose initialization
    if not isinstance(P0, str):
        P0 = np.atleast_2d(P0)
        if P0.shape != (n_unseed, n_unseed):
            msg = "`P0` matrix must have shape m' x m', where m'=n-m"
        elif ((P0 < 0).any() or not np.allclose(np.sum(P0, axis=0), 1)
              or not np.allclose(np.sum(P0, axis=1), 1)):
            msg = "`P0` matrix must be doubly stochastic"
        if msg is not None:
            raise ValueError(msg)
    elif P0 == 'barycenter':
        P0 = np.ones((n_unseed, n_unseed)) / n_unseed
    elif P0 == 'randomized':
        J = np.ones((n_unseed, n_unseed)) / n_unseed
        # generate a nxn matrix where each entry is a random number [0, 1]
        # would use rand, but Generators don't have it
        # would use random, but old mtrand.RandomStates don't have it
        K = _doubly_stochastic(rng.uniform(size=(n_unseed, n_unseed)))
        P0 = (J + K) / 2

    # check trivial cases
    if n == 0 or n_seeds == n:
        score = _calc_score(A, B, partial_match[:, 1])
        res = {"col_ind": partial_match[:, 1], "fun": score, "nit": 0}
        return OptimizeResult(res)

    obj_func_scalar = 1
    if maximize:
        obj_func_scalar = -1

    nonseed_B = np.setdiff1d(range(n), partial_match[:, 1])
    if shuffle_input:
        nonseed_B = rng.permutation(nonseed_B)

    nonseed_A = np.setdiff1d(range(n), partial_match[:, 0])
    perm_A = np.concatenate([partial_match[:, 0], nonseed_A])
    perm_B = np.concatenate([partial_match[:, 1], nonseed_B])

    # definitions according to Seeded Graph Matching [2].
    A11, A12, A21, A22 = _split_matrix(A[perm_A][:, perm_A], n_seeds)
    B11, B12, B21, B22 = _split_matrix(B[perm_B][:, perm_B], n_seeds)
    const_sum = A21 @ B21.T + A12.T @ B12

    P = P0
    # [1] Algorithm 1 Line 2 - loop while stopping criteria not met
    for n_iter in range(1, maxiter+1):
        # [1] Algorithm 1 Line 3 - compute the gradient of f(P) = -tr(APB^tP^t)
        grad_fp = (const_sum + A22 @ P @ B22.T + A22.T @ P @ B22)
        # [1] Algorithm 1 Line 4 - get direction Q by solving Eq. 8
        _, cols = linear_sum_assignment(grad_fp, maximize=maximize)
        Q = np.eye(n_unseed)[cols]

        # [1] Algorithm 1 Line 5 - compute the step size
        # Noting that e.g. trace(Ax) = trace(A)*x, expand and re-collect
        # terms as ax**2 + bx + c. c does not affect location of minimum
        # and can be ignored. Also, note that trace(A@B) = (A.T*B).sum();
        # apply where possible for efficiency.
        R = P - Q
        b21 = ((R.T @ A21) * B21).sum()
        b12 = ((R.T @ A12.T) * B12.T).sum()
        AR22 = A22.T @ R
        BR22 = B22 @ R.T
        b22a = (AR22 * B22.T[cols]).sum()
        b22b = (A22 * BR22[cols]).sum()
        a = (AR22.T * BR22).sum()
        b = b21 + b12 + b22a + b22b
        # critical point of ax^2 + bx + c is at x = -d/(2*e)
        # if a * obj_func_scalar > 0, it is a minimum
        # if minimum is not in [0, 1], only endpoints need to be considered
        if a*obj_func_scalar > 0 and 0 <= -b/(2*a) <= 1:
            alpha = -b/(2*a)
        else:
            alpha = np.argmin([0, (b + a)*obj_func_scalar])

        # [1] Algorithm 1 Line 6 - Update P
        P_i1 = alpha * P + (1 - alpha) * Q
        if np.linalg.norm(P - P_i1) / np.sqrt(n_unseed) < tol:
            P = P_i1
            break
        P = P_i1
    # [1] Algorithm 1 Line 7 - end main loop

    # [1] Algorithm 1 Line 8 - project onto the set of permutation matrices
    _, col = linear_sum_assignment(P, maximize=True)
    perm = np.concatenate((np.arange(n_seeds), col + n_seeds))

    unshuffled_perm = np.zeros(n, dtype=int)
    unshuffled_perm[perm_A] = perm_B[perm]

    score = _calc_score(A, B, unshuffled_perm)
    res = {"col_ind": unshuffled_perm, "fun": score, "nit": n_iter}
    return OptimizeResult(res)

