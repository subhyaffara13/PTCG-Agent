
def qrexc_Rdiag(A, Q, Rdiag, i):  # Used in COBYLA
    '''
    This function updates the QR factorization for an MxN matrix A=Q@R so that the updated Q and
    R form a QR factorization of [A_0, ..., A_{I-1}, A_{I+1}, ..., A_{N-1}, A_I] which is the matrix
    obtained by rearranging columns [I, I+1, ... N-1] of A to [I+1, ..., N-1, I]. Here A is ASSUMED TO
    BE OF FULL COLUMN RANK, Q is a matrix whose columns are orthogonal, and R, which is not present,
    is an upper triangular matrix whose diagonal entries are nonzero. Q and R need not be square.
    N.B.:
    0. Instead of R, this function updates Rdiag, which is np.diag(R), the size being n.
    1. With L = Q.shape[1] = R.shape[0], we have M >= L >= N. Most often L = M or N.
    2. This function changes only Q[:, i:] and Rdiag[i:]
    3. (NDB 20230919) In Python, i is either icon or nact - 2, whereas in FORTRAN it is either icon or nact - 1.
    '''

    # Sizes
    m, n = A.shape

    # Preconditions
    assert n >= 1 and n <= m
    assert i >= 0 and i < n
    assert len(Rdiag) == n
    assert Q.shape[0] == m and Q.shape[1] >= n and Q.shape[1] <= m
    # tol = max(1.0E-8, min(1.0E-1, 1.0E8 * EPS * m + 1))
    # assert isorth(Q, tol)  # Costly!


    if i < 0 or i >= n:
        return Q, Rdiag

    # Let R be the upper triangular matrix in the QR factorization, namely R = Q.T@A.
    # For each k, find the Givens rotation G with G@(R[k:k+2, :]) = [hypt, 0], and update Q[:, k:k+2]
    # to Q[:, k:k+2]@(G.T). Then R = Q.T@A is an upper triangular matrix as long as A[:, [k, k+1]] is
    # updated to A[:, [k+1, k]]. Indeed, this new upper triangular matrix can be obtained by first
    # updating R[[k, k+1], :] to G@(R[[k, k+1], :]) and then exchanging its columns K and K+1; at the same
    # time, entries k and k+1 of R's diagonal Rdiag become [hypt, -(Rdiag[k+1]/hypt)*RDiag[k]].
    # After this is done for each k = 0, ..., n-2, we obtain the QR factorization of the matrix that
    # rearranges columns [i, i+1, ... n-1] of A as [i+1, ..., n-1, i].
    # Powell's code, however, is slightly different: before everything, he first exchanged columns k and
    # k+1 of Q (as well as rows k and k+1 of R). This makes sure that the entries of the update Rdiag
    # are all positive if it is the case for the original Rdiag.
    for k in range(i, n-1):
        G = planerot([Rdiag[k+1], inprod(Q[:, k], A[:, k+1])])
        Q[:, [k, k+1]] = matprod(Q[:, [k+1, k]], (G.T))
        # Powell's code updates Rdiag in the following way:
        # hypt = np.sqrt(Rdiag[k+1]**2 + np.dot(Q[:, k], A[:, k+1])**2)
        # Rdiag[[k, k+1]] = [hypt, (Rdiag[k+1]/hypt)*Rdiag[k]]
        # Note that Rdiag[n-1] inherits all rounding in Rdiag[i:n-1] and Q[:, i:n-1] and hence contains
        # significant errors. Thus we may modify Powell's code to set only Rdiag[k] = hypt here and then
        # calculate Rdiag[n] by an inner product after the loop. Nevertheless, we simple calculate RDiag
        # from scratch below.

    # Calculate Rdiag(i:n) from scratch
    Rdiag[i:n-1] = [inprod(Q[:, k], A[:, k+1]) for k in range(i, n-1)]
    Rdiag[n-1] = inprod(Q[:, n-1], A[:, i])

    return Q, Rdiag

