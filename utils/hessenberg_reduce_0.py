
def hessenberg_reduce_0(ctx, A, T):
    """
    This routine computes the (upper) Hessenberg decomposition of a square matrix A.
    Given A, an unitary matrix Q is calculated such that

               Q' A Q = H              and             Q' Q = Q Q' = 1

    where H is an upper Hessenberg matrix, meaning that it only contains zeros
    below the first subdiagonal. Here ' denotes the hermitian transpose (i.e.
    transposition and conjugation).

    parameters:
      A         (input/output) On input, A contains the square matrix A of
                dimension (n,n). On output, A contains a compressed representation
                of Q and H.
      T         (output) An array of length n containing the first elements of
                the Householder reflectors.
    """

    # internally we work with householder reflections from the right.
    # let u be a row vector (i.e. u[i]=A[i,:i]). then
    # Q is build up by reflectors of the type (1-v'v) where v is a suitable
    # modification of u. these reflectors are applyed to A from the right.
    # because we work with reflectors from the right we have to start with
    # the bottom row of A and work then upwards (this corresponds to
    # some kind of RQ decomposition).
    # the first part of the vectors v (i.e. A[i,:(i-1)]) are stored as row vectors
    # in the lower left part of A (excluding the diagonal and subdiagonal).
    # the last entry of v is stored in T.
    # the upper right part of A (including diagonal and subdiagonal) becomes H.


    n = A.rows
    if n <= 2: return

    for i in xrange(n-1, 1, -1):

        # scale the vector

        scale = 0
        for k in xrange(0, i):
            scale += abs(ctx.re(A[i,k])) + abs(ctx.im(A[i,k]))

        scale_inv = 0
        if scale != 0:
            scale_inv = 1 / scale

        if scale == 0 or ctx.isinf(scale_inv):
            # sadly there are floating point numbers not equal to zero whose reciprocal is infinity
            T[i] = 0
            A[i,i-1] = 0
            continue

        # calculate parameters for housholder transformation

        H = 0
        for k in xrange(0, i):
            A[i,k] *= scale_inv
            rr = ctx.re(A[i,k])
            ii = ctx.im(A[i,k])
            H += rr * rr + ii * ii

        F = A[i,i-1]
        f = abs(F)
        G = ctx.sqrt(H)
        A[i,i-1] = - G * scale

        if f == 0:
            T[i] = G
        else:
            ff = F / f
            T[i] = F + G * ff
            A[i,i-1] *= ff

        H += G * f
        H = 1 / ctx.sqrt(H)

        T[i] *= H
        for k in xrange(0, i - 1):
            A[i,k] *= H

        for j in xrange(0, i):
            # apply housholder transformation (from right)

            G = ctx.conj(T[i]) * A[j,i-1]
            for k in xrange(0, i-1):
                G += ctx.conj(A[i,k]) * A[j,k]

            A[j,i-1] -= G * T[i]
            for k in xrange(0, i-1):
                A[j,k] -= G * A[i,k]

        for j in xrange(0, n):
            # apply housholder transformation (from left)

            G = T[i] * A[i-1,j]
            for k in xrange(0, i-1):
                G += A[i,k] * A[k,j]

            A[i-1,j] -= G * ctx.conj(T[i])
            for k in xrange(0, i-1):
                A[k,j] -= G * ctx.conj(A[i,k])

