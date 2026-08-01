
def abcd_normalize(A=None, B=None, C=None, D=None):
    r"""Check state-space matrices compatibility and ensure they are 2d arrays.

    First, the input matrices are converted into two-dimensional arrays with
    appropriate dtype as needed. Then the dimensions n, q, p are determined by
    investigating the array shapes. If an input is ``None``, or has size zero, it is
    set to an array of zeros of compatible shape. Finally, it is verified that all
    parameter shapes are compatible with each other. If that fails, a ``ValueError`` is
    raised. Note that the dimensions n, q, p are allowed to be zero.

    Parameters
    ----------
    A : array_like, optional
        Two-dimensional array of shape (n, n).
    B : array_like, optional
        Two-dimensional array of shape (n, p).
    C : array_like, optional
        Two-dimensional array of shape (q, n).
    D : array_like, optional
        Two-dimensional array of shape (q, p).

    Returns
    -------
    A, B, C, D : array
        State-space matrices as two-dimensional arrays with identical dtype.
        The result dtype is determined based on the standard
        `dtype promotion rules <https://numpy.org/doc/2.3/reference/arrays.promotion.html>`_
        except for when the inputs are all of integer dtype, in which case the returned
        arrays will have the default floating point dtype of ``float64``.

    Raises
    ------
    ValueError
        If the dimensions n, q, or p could not be determined or if the shapes are
        incompatible with each other.

    Notes
    -----
    If a matrix is not modified, the original matrix (not a copy) is returned.

    The :ref:`tutorial_signal_state_space_representation` section of the
    :ref:`user_guide` presents the corresponding definitions of continuous-time and
    disrcete time state space systems.

    See Also
    --------
    StateSpace: Linear Time Invariant system in state-space form.
    dlti: Discrete-time linear time invariant system base class.
    tf2ss: Transfer function to state-space representation.
    ss2tf: State-space to transfer function.
    ss2zpk: State-space representation to zero-pole-gain representation.
    cont2discrete: Transform a continuous to a discrete state-space system.

    Examples
    --------
    The following example demonstrates that the passed lists are converted into
    two-dimensional arrays:

    >>> from scipy.signal import abcd_normalize
    >>> AA, BB, CC, DD = abcd_normalize(A=[[1, 2], [3, 4]], B=[[-1], [5]],
    ...                                 C=[[4, 5]], D=2.5)
    >>> AA.shape, BB.shape, CC.shape, DD.shape
    ((2, 2), (2, 1), (1, 2), (1, 1))

    In the following, the missing parameter C is assumed to be an array of zeros
    with shape (1, 2):

    >>> from scipy.signal import abcd_normalize
    >>> AA, BB, CC, DD = abcd_normalize(A=[[1, 2], [3, 4]], B=[[-1], [5]], D=2.5)
    >>> AA.shape, BB.shape, CC.shape, DD.shape
    ((2, 2), (2, 1), (1, 2), (1, 1))
    >>> CC
    array([[0., 0.]])

    """
    if A is None and B is None and C is None:
        raise ValueError("Dimension n is undefined for parameters A = B = C = None!")
    if B is None and D is None:
        raise ValueError("Dimension p is undefined for parameters B = D = None!")
    if C is None and D is None:
        raise ValueError("Dimension q is undefined for parameters C = D = None!")

    xp = array_namespace(A, B, C, D)
    A, B, C, D = xp_promote(A, B, C, D, xp=xp, force_floating=True)
    dtype = xp_result_type(A, B, C, D, xp=xp)

    # convert inputs into 2d arrays (zero-size 2d array if None):
    A, B, C, D = (
        xpx.atleast_nd(xp.asarray(M_), ndim=2, xp=xp)
        if M_ is not None else xp.zeros((0, 0), dtype=dtype)
        for M_ in (A, B, C, D)
    )

    n = A.shape[0] or B.shape[0] or C.shape[1] # try finding non-zero dimensions
    p = B.shape[1] or D.shape[1]
    q = C.shape[0] or D.shape[0]

    # Create zero matrices as needed:
    A = xp.zeros((n, n), dtype=dtype) if xp_size(A) == 0 else A
    B = xp.zeros((n, p), dtype=dtype) if xp_size(B) == 0 else B
    C = xp.zeros((q, n), dtype=dtype) if xp_size(C) == 0 else C
    D = xp.zeros((q, p), dtype=dtype) if xp_size(D) == 0 else D

    if A.shape != (n, n):
        raise ValueError(f"Parameter A has shape {A.shape} but should be ({n}, {n})!")
    if B.shape != (n, p):
        raise ValueError(f"Parameter B has shape {B.shape} but should be ({n}, {p})!")
    if C.shape != (q, n):
        raise ValueError(f"Parameter C has shape {C.shape} but should be ({q}, {n})!")
    if D.shape != (q, p):
        raise ValueError(f"Parameter D has shape {D.shape} but should be ({q}, {p})!")

    return A, B, C, D

