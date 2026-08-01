
def sylvester(f, g, x, method = 1):
    '''
      The input polynomials f, g are in Z[x] or in Q[x]. Let m = degree(f, x),
      n = degree(g, x) and mx = max(m, n).

      a. If method = 1 (default), computes sylvester1, Sylvester's matrix of 1840
          of dimension (m + n) x (m + n). The determinants of properly chosen
          submatrices of this matrix (a.k.a. subresultants) can be
          used to compute the coefficients of the Euclidean PRS of f, g.

      b. If method = 2, computes sylvester2, Sylvester's matrix of 1853
          of dimension (2*mx) x (2*mx). The determinants of properly chosen
          submatrices of this matrix (a.k.a. ``modified'' subresultants) can be
          used to compute the coefficients of the Sturmian PRS of f, g.

      Applications of these Matrices can be found in the references below.
      Especially, for applications of sylvester2, see the first reference!!

      References
      ==========
      1. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``On a Theorem
      by Van Vleck Regarding Sturm Sequences. Serdica Journal of Computing,
      Vol. 7, No 4, 101-134, 2013.

      2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Sturm Sequences
      and Modified Subresultant Polynomial Remainder Sequences.''
      Serdica Journal of Computing, Vol. 8, No 1, 29-46, 2014.

    '''
    # obtain degrees of polys
    m, n = degree( Poly(f, x), x), degree( Poly(g, x), x)

    # Special cases:
    # A:: case m = n < 0 (i.e. both polys are 0)
    if m == n and n < 0:
        return Matrix([])

    # B:: case m = n = 0  (i.e. both polys are constants)
    if m == n and n == 0:
        return Matrix([])

    # C:: m == 0 and n < 0 or m < 0 and n == 0
    # (i.e. one poly is constant and the other is 0)
    if m == 0 and n < 0:
        return Matrix([])
    elif m < 0 and n == 0:
        return Matrix([])

    # D:: m >= 1 and n < 0 or m < 0 and n >=1
    # (i.e. one poly is of degree >=1 and the other is 0)
    if m >= 1 and n < 0:
        return Matrix([0])
    elif m < 0 and n >= 1:
        return Matrix([0])

    fp = Poly(f, x).all_coeffs()
    gp = Poly(g, x).all_coeffs()

    # Sylvester's matrix of 1840 (default; a.k.a. sylvester1)
    if method <= 1:
        M = zeros(m + n)
        k = 0
        for i in range(n):
            j = k
            for coeff in fp:
                M[i, j] = coeff
                j = j + 1
            k = k + 1
        k = 0
        for i in range(n, m + n):
            j = k
            for coeff in gp:
                M[i, j] = coeff
                j = j + 1
            k = k + 1
        return M

    # Sylvester's matrix of 1853 (a.k.a sylvester2)
    else:
        if len(fp) < len(gp):
            h = []
            for i in range(len(gp) - len(fp)):
                h.append(0)
            fp[ : 0] = h
        else:
            h = []
            for i in range(len(fp) - len(gp)):
                h.append(0)
            gp[ : 0] = h
        mx = max(m, n)
        dim = 2*mx
        M = zeros( dim )
        k = 0
        for i in range( mx ):
            j = k
            for coeff in fp:
                M[2*i, j] = coeff
                j = j + 1
            j = k
            for coeff in gp:
                M[2*i + 1, j] = coeff
                j = j + 1
            k = k + 1
        return M

