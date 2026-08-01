
def subspace_angles(A, B):
    r"""
    Compute the subspace angles between two matrices.

    Parameters
    ----------
    A : (M, N) array_like
        The first input array.
    B : (M, K) array_like
        The second input array.

    Returns
    -------
    angles : ndarray, shape (min(N, K),)
        The subspace angles between the column spaces of `A` and `B` in
        descending order.

    See Also
    --------
    orth
    svd

    Notes
    -----
    This computes the subspace angles according to the formula
    provided in [1]_. For equivalence with MATLAB and Octave behavior,
    use ``angles[0]``.

    .. versionadded:: 1.0

    References
    ----------
    .. [1] Knyazev A, Argentati M (2002) Principal Angles between Subspaces
           in an A-Based Scalar Product: Algorithms and Perturbation
           Estimates. SIAM J. Sci. Comput. 23:2008-2040.

    Examples
    --------
    A Hadamard matrix, which has orthogonal columns, so we expect that
    the subspace angle to be :math:`\frac{\pi}{2}`:

    >>> import numpy as np
    >>> from scipy.linalg import hadamard, subspace_angles
    >>> rng = np.random.default_rng()
    >>> H = hadamard(4)
    >>> print(H)
    [[ 1  1  1  1]
     [ 1 -1  1 -1]
     [ 1  1 -1 -1]
     [ 1 -1 -1  1]]
    >>> np.rad2deg(subspace_angles(H[:, :2], H[:, 2:]))
    array([ 90.,  90.])

    And the subspace angle of a matrix to itself should be zero:

    >>> subspace_angles(H[:, :2], H[:, :2]) <= 2 * np.finfo(float).eps
    array([ True,  True], dtype=bool)

    The angles between non-orthogonal subspaces are in between these extremes:

    >>> x = rng.standard_normal((4, 3))
    >>> np.rad2deg(subspace_angles(x[:, :2], x[:, [2]]))
    array([ 55.832])  # random
    """
    # Steps here omit the U and V calculation steps from the paper

    # 1. Compute orthonormal bases of column-spaces
    A = _asarray_validated(A, check_finite=True)
    if len(A.shape) != 2:
        raise ValueError(f'expected 2D array, got shape {A.shape}')
    QA = orth(A)
    del A

    B = _asarray_validated(B, check_finite=True)
    if len(B.shape) != 2:
        raise ValueError(f'expected 2D array, got shape {B.shape}')
    if len(B) != len(QA):
        raise ValueError('A and B must have the same number of rows, got '
                         f'{QA.shape[0]} and {B.shape[0]}')
    QB = orth(B)
    del B

    # 2. Compute SVD for cosine
    QA_H_QB = np.dot(QA.T.conj(), QB)
    sigma = svdvals(QA_H_QB)

    # 3. Compute matrix B
    if QA.shape[1] >= QB.shape[1]:
        B = QB - np.dot(QA, QA_H_QB)
    else:
        B = QA - np.dot(QB, QA_H_QB.T.conj())
    del QA, QB, QA_H_QB

    # 4. Compute SVD for sine
    mask = sigma ** 2 >= 0.5
    if mask.any():
        mu_arcsin = np.arcsin(np.clip(svdvals(B, overwrite_a=True), -1., 1.))
    else:
        mu_arcsin = 0.

    # 5. Compute the principal angles
    # with reverse ordering of sigma because smallest sigma belongs to largest
    # angle theta
    theta = np.where(mask, mu_arcsin, np.arccos(np.clip(sigma[::-1], -1., 1.)))
    return theta

