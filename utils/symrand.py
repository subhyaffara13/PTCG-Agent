
def symrand(dim_or_eigv, rng):
    """Return a random symmetric (Hermitian) matrix.

    If 'dim_or_eigv' is an integer N, return a NxN matrix, with eigenvalues
        uniformly distributed on (-1,1).

    If 'dim_or_eigv' is  1-D real array 'a', return a matrix whose
                      eigenvalues are 'a'.
    """
    if isinstance(dim_or_eigv, int):
        dim = dim_or_eigv
        d = rng.random(dim)*2 - 1
    elif (isinstance(dim_or_eigv, ndarray) and
          len(dim_or_eigv.shape) == 1):
        dim = dim_or_eigv.shape[0]
        d = dim_or_eigv
    else:
        raise TypeError("input type not supported.")

    v = ortho_group.rvs(dim)
    h = v.T.conj() @ diag(d) @ v
    # to avoid roundoff errors, symmetrize the matrix (again)
    h = 0.5*(h.T+h)
    return h

