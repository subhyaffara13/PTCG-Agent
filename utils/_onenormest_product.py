
def _onenormest_product(operator_seq,
        t=2, itmax=5, compute_v=False, compute_w=False, structure=None):
    """
    Efficiently estimate the 1-norm of the matrix product of the args.

    Parameters
    ----------
    operator_seq : linear operator sequence
        Matrices whose 1-norm of product is to be computed.
    t : int, optional
        A positive parameter controlling the tradeoff between
        accuracy versus time and memory usage.
        Larger values take longer and use more memory
        but give more accurate output.
    itmax : int, optional
        Use at most this many iterations.
    compute_v : bool, optional
        Request a norm-maximizing linear operator input vector if True.
    compute_w : bool, optional
        Request a norm-maximizing linear operator output vector if True.
    structure : str, optional
        A string describing the structure of all operators.
        Only `upper_triangular` is currently supported.

    Returns
    -------
    est : float
        An underestimate of the 1-norm of the sparse arrays.
    v : ndarray, optional
        The vector such that ||Av||_1 == est*||v||_1.
        It can be thought of as an input to the linear operator
        that gives an output with particularly large norm.
    w : ndarray, optional
        The vector Av which has relatively large 1-norm.
        It can be thought of as an output of the linear operator
        that is relatively large in norm compared to the input.

    """
    return scipy.sparse.linalg.onenormest(
            ProductOperator(*operator_seq, structure=structure))

