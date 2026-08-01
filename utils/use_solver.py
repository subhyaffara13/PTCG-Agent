
def use_solver(**kwargs):
    """
    Select default sparse direct solver to be used.

    Parameters
    ----------
    **kwargs
        The following options may be passed as keyword arguments.

        useUmfpack : bool, optional
            Use UMFPACK [1]_, [2]_, [3]_, [4]_. over SuperLU. Has effect only
            if ``scikits.umfpack`` is installed. Default: True
        assumeSortedIndices : bool, optional
            Allow UMFPACK to skip the step of sorting indices for a CSR/CSC matrix.
            Has effect only if useUmfpack is True and ``scikits.umfpack`` is
            installed. Default: False

    Notes
    -----
    The default sparse solver is UMFPACK when available
    (``scikits.umfpack`` is installed). This can be changed by passing
    useUmfpack = False, which then causes the always present SuperLU
    based solver to be used.

    UMFPACK requires a CSR/CSC matrix to have sorted column/row indices. If
    sure that the matrix fulfills this, pass ``assumeSortedIndices=True``
    to gain some speed.

    References
    ----------
    .. [1] T. A. Davis, Algorithm 832:  UMFPACK - an unsymmetric-pattern
           multifrontal method with a column pre-ordering strategy, ACM
           Trans. on Mathematical Software, 30(2), 2004, pp. 196--199.
           :doi:`10.1145/992200.992206`.

    .. [2] T. A. Davis, A column pre-ordering strategy for the
           unsymmetric-pattern multifrontal method, ACM Trans.
           on Mathematical Software, 30(2), 2004, pp. 165--195.
           :doi:`10.1145/992200.992205`.

    .. [3] T. A. Davis and I. S. Duff, A combined unifrontal/multifrontal
           method for unsymmetric sparse matrices, ACM Trans. on
           Mathematical Software, 25(1), 1999, pp. 1--19.
           :doi:`10.1145/305658.287640`.

    .. [4] T. A. Davis and I. S. Duff, An unsymmetric-pattern multifrontal
           method for sparse LU factorization, SIAM J. Matrix Analysis and
           Computations, 18(1), 1997, pp. 140--158.
           :doi:`10.1137/S0895479894246905T`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse.linalg import use_solver, spsolve
    >>> from scipy.sparse import csc_array
    >>> R = np.random.randn(5, 5)
    >>> A = csc_array(R)
    >>> b = np.random.randn(5)
    >>> use_solver(useUmfpack=False) # enforce superLU over UMFPACK
    >>> x = spsolve(A, b)
    >>> np.allclose(A.dot(x), b)
    True
    >>> use_solver(useUmfpack=True) # reset umfPack usage to default
    """
    global useUmfpack
    if 'useUmfpack' in kwargs:
        useUmfpack.u = kwargs['useUmfpack']
    if useUmfpack.u and 'assumeSortedIndices' in kwargs:
        umfpack.configure(assumeSortedIndices=kwargs['assumeSortedIndices'])

