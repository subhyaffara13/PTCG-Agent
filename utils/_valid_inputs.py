
def _valid_inputs(A, B, poles, method, rtol, maxiter):
    """
    Check the poles come in complex conjugate pairs
    Check shapes of A, B and poles are compatible.
    Check the method chosen is compatible with provided poles
    Return update method to use and ordered poles

    """
    poles = np.asarray(poles)
    if poles.ndim > 1:
        raise ValueError("Poles must be a 1D array like.")
    # Will raise ValueError if poles do not come in complex conjugates pairs
    poles = _order_complex_poles(poles)
    if A.ndim > 2:
        raise ValueError("A must be a 2D array/matrix.")
    if B.ndim > 2:
        raise ValueError("B must be a 2D array/matrix")
    if A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")
    if len(poles) > A.shape[0]:
        raise ValueError(
            f"maximum number of poles is {A.shape[0]} but you asked for {len(poles)}"
        )
    if len(poles) < A.shape[0]:
        raise ValueError(
            f"number of poles is {len(poles)} but you should provide {A.shape[0]}"
        )
    r = np.linalg.matrix_rank(B)
    for p in poles:
        if sum(p == poles) > r:
            raise ValueError("at least one of the requested pole is repeated "
                             "more than rank(B) times")
    # Choose update method
    update_loop = _YT_loop
    if method not in ('KNV0','YT'):
        raise ValueError("The method keyword must be one of 'YT' or 'KNV0'")

    if method == "KNV0":
        update_loop = _KNV0_loop
        if not all(np.isreal(poles)):
            raise ValueError("Complex poles are not supported by KNV0")

    if maxiter < 1:
        raise ValueError("maxiter must be at least equal to 1")

    # We do not check rtol <= 0 as the user can use a negative rtol to
    # force maxiter iterations
    if rtol > 1:
        raise ValueError("rtol can not be greater than 1")

    return update_loop, poles

