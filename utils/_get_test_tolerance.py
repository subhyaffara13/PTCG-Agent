
def _get_test_tolerance(type_char, mattype=None, D_type=None, which=None):
    """
    Return tolerance values suitable for a given test:

    Parameters
    ----------
    type_char : {'f', 'd', 'F', 'D'}
        Data type in ARPACK eigenvalue problem
    mattype : {csr_array, aslinearoperator, asarray}, optional
        Linear operator type

    Returns
    -------
    tol
        Tolerance to pass to the ARPACK routine
    rtol
        Relative tolerance for outputs
    atol
        Absolute tolerance for outputs

    """

    rtol = {'f': 3000 * np.finfo(np.float32).eps,
            'F': 3000 * np.finfo(np.float32).eps,
            'd': 2000 * np.finfo(np.float64).eps,
            'D': 2000 * np.finfo(np.float64).eps}[type_char]
    atol = rtol
    tol = 0

    if mattype is aslinearoperator and type_char in ('f', 'F'):
        # iterative methods in single precision: worse errors
        # also: bump ARPACK tolerance so that the iterative method converges
        tol = 30 * np.finfo(np.float32).eps
        rtol *= 5

    if (
        isinstance(mattype, type) and issubclass(mattype, csr_array)
        and type_char in ('f', 'F')
    ):
        # sparse in single precision: worse errors
        rtol *= 5

    if (
        which in ('LM', 'SM', 'LA')
        and D_type.name == "gen-hermitian-Mc"
    ):
        if type_char == 'F':
            # missing case 1, 2, and more, from PR 14798
            rtol *= 5

        if type_char == 'D':
            # missing more cases, from PR 14798
            rtol *= 10
            atol *= 10

    return tol, rtol, atol

