
def trstlp(A, b, delta, g):
    '''
    This function calculated an n-component vector d by the following two stages. In the first
    stage, d is set to the shortest vector that minimizes the greatest violation of the constraints
        A.T @ D <= B,  K = 1, 2, 3, ..., M,
    subject to the Euclidean length of d being at most delta. If its length is strictly less than
    delta, then the second stage uses the resultant freedom in d to minimize the objective function
        G.T @ D
    subject to no increase in any greatest constraint violation.

    It is possible but rare that a degeneracy may prevent d from attaining the target length delta.

    cviol is the largest constraint violation of the current d: max(max(A.T@D - b), 0)
    icon is the index of a most violated constraint if cviol is positive.

    nact is the number of constraints in the active set and iact[0], ..., iact[nact-1] are their indices,
    while the remainder of the iact contains a permutation of the remaining constraint indicies.
    N.B.: nact <= min(num_constraints, num_vars). Obviously nact <= num_constraints. In addition, the constraints
    in iact[0, ..., nact-1] have linearly independent gradients (see the comments above the instruction
    that delete a constraint from the active set to make room for the new active constraint with index iact[icon]);
    it can also be seen from the update of nact: starting from 0, nact is incremented only if nact < n.

    Further, Z is an orthogonal matrix whose first nact columns can be regarded as the result of
    Gram-Schmidt applied to the active constraint gradients. For j = 0, 1, ..., nact-1, the number
    zdota[j] is the scalar product of the jth column of Z with the gradient of the jth active
    constraint. d is the current vector of variables and here the residuals of the active constraints
    should be zero. Further, the active constraints have nonnegative Lagrange multipliers that are
    held at the beginning of vmultc. The remainder of this vector holds the residuals of the inactive
    constraints at d, the ordering of the components of vmultc being in agreement with the permutation
    of the indices of the constraints that is in iact. All these residuals are nonnegative, which is
    achieved by the shift cviol that makes the least residual zero.

    N.B.:
    0. In Powell's implementation, the constraints are A.T @ D >= B. In other words, the A and B in
    our implementation are the negative of those in Powell's implementation.
    1. The algorithm was NOT documented in the COBYLA paper. A note should be written to introduce it!
    2. As a major part of the algorithm (see trstlp_sub), the code maintains and updates the QR
    factorization of A[iact[:nact]], i.e. the gradients of all the active (linear) constraints. The
    matrix Z is indeed Q, and the vector zdota is the diagonal of R. The factorization is updated by
    Givens rotations when an index is added in or removed from iact.
    3. There are probably better algorithms available for the trust-region linear programming problem.
    '''

    # Sizes
    num_constraints = A.shape[1]
    num_vars = A.shape[0]

    # Preconditions
    if DEBUGGING:
        assert num_vars >= 1
        assert num_constraints >= 0
        assert np.size(g) == num_vars
        assert np.size(b) == num_constraints
        assert delta > 0


    vmultc = np.zeros(num_constraints + 1)
    iact = np.zeros(num_constraints + 1, dtype=int)
    nact = 0
    d = np.zeros(num_vars)
    z = np.zeros((num_vars, num_vars))

    # ==================
    # Calculation starts
    # ==================

    # Form A_aug and B_aug. This allows the gradient of the objective function to be regarded as the
    # gradient of a constraint in the second stage.
    A_aug = np.hstack([A, g.reshape((num_vars, 1))])
    b_aug = np.hstack([b, 0])


    # Scale the problem if A contains large values. Otherwise floating point exceptions may occur.
    # Note that the trust-region step is scale invariant.
    for i in range(num_constraints+1):  # Note that A_aug.shape[1] == num_constraints+1
        if (maxval:=max(abs(A_aug[:, i]))) > 1e12:
            modscal = max(2*REALMIN, 1/maxval)
            A_aug[:, i] *= modscal
            b_aug[i] *= modscal

    # Stage 1: minimize the 1+infinity constraint violation of the linearized constraints.
    iact[:num_constraints], nact, d, vmultc[:num_constraints], z = trstlp_sub(iact[:num_constraints], nact, 1, A_aug[:, :num_constraints], b_aug[:num_constraints], delta, d, vmultc[:num_constraints], z)

    # Stage 2: minimize the linearized objective without increasing the 1_infinity constraint violation.
    iact, nact, d, vmultc, z = trstlp_sub(iact, nact, 2, A_aug, b_aug, delta, d, vmultc, z)

    # ================
    # Calculation ends
    # ================

    # Postconditions
    if DEBUGGING:
        assert all(np.isfinite(d))
        # Due to rounding, it may happen that ||D|| > DELTA, but ||D|| > 2*DELTA is highly improbable.
        assert np.linalg.norm(d) <= 2 * delta

    return d

