
def cdf2rdf(w, v):
    """
    Complex diagonal form to real diagonal block form.

    Converts complex eigenvalues ``w`` and eigenvectors ``v`` to real
    eigenvalues in a block diagonal form ``wr`` and the associated real
    eigenvectors ``vr``, such that::

        vr @ wr = X @ vr

    continues to hold, where ``X`` is the original array for which ``w`` and
    ``v`` are the eigenvalues and eigenvectors.

    .. versionadded:: 1.1.0

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    w : (..., M) array_like
        Complex or real eigenvalues, an array or stack of arrays

        Conjugate pairs must not be interleaved, else the wrong result
        will be produced. So ``[1+1j, 1, 1-1j]`` will give a correct result,
        but ``[1+1j, 2+1j, 1-1j, 2-1j]`` will not.

    v : (..., M, M) array_like
        Complex or real eigenvectors, a square array or stack of square arrays.

    Returns
    -------
    wr : (..., M, M) ndarray
        Real diagonal block form of eigenvalues
    vr : (..., M, M) ndarray
        Real eigenvectors associated with ``wr``

    See Also
    --------
    eig : Eigenvalues and right eigenvectors for non-symmetric arrays
    rsf2csf : Convert real Schur form to complex Schur form

    Notes
    -----
    ``w``, ``v`` must be the eigenstructure for some *real* matrix ``X``.
    For example, obtained by ``w, v = scipy.linalg.eig(X)`` or
    ``w, v = numpy.linalg.eig(X)`` in which case ``X`` can also represent
    stacked arrays.

    .. versionadded:: 1.1.0

    Examples
    --------
    >>> import numpy as np
    >>> X = np.array([[1, 2, 3], [0, 4, 5], [0, -5, 4]])
    >>> X
    array([[ 1,  2,  3],
           [ 0,  4,  5],
           [ 0, -5,  4]])

    >>> from scipy import linalg
    >>> w, v = linalg.eig(X)
    >>> w
    array([ 1.+0.j,  4.+5.j,  4.-5.j])
    >>> v
    array([[ 1.00000+0.j     , -0.01906-0.40016j, -0.01906+0.40016j],
           [ 0.00000+0.j     ,  0.00000-0.64788j,  0.00000+0.64788j],
           [ 0.00000+0.j     ,  0.64788+0.j     ,  0.64788-0.j     ]])

    >>> wr, vr = linalg.cdf2rdf(w, v)
    >>> wr
    array([[ 1.,  0.,  0.],
           [ 0.,  4.,  5.],
           [ 0., -5.,  4.]])
    >>> vr
    array([[ 1.     ,  0.40016, -0.01906],
           [ 0.     ,  0.64788,  0.     ],
           [ 0.     ,  0.     ,  0.64788]])

    >>> vr @ wr
    array([[ 1.     ,  1.69593,  1.9246 ],
           [ 0.     ,  2.59153,  3.23942],
           [ 0.     , -3.23942,  2.59153]])
    >>> X @ vr
    array([[ 1.     ,  1.69593,  1.9246 ],
           [ 0.     ,  2.59153,  3.23942],
           [ 0.     , -3.23942,  2.59153]])
    """
    w, v = _asarray_validated(w), _asarray_validated(v)
    _deprecate_dtypes("cdf2rdf", w, v)

    # check dimensions
    if w.ndim < 1:
        raise ValueError('expected w to be at least 1D')
    if v.ndim < 2:
        raise ValueError('expected v to be at least 2D')
    if v.ndim != w.ndim + 1:
        raise ValueError('expected eigenvectors array to have exactly one '
                         'dimension more than eigenvalues array')

    # check shapes
    n = w.shape[-1]
    M = w.shape[:-1]
    if v.shape[-2] != v.shape[-1]:
        raise ValueError('expected v to be a square matrix or stacked square '
                         'matrices: v.shape[-2] = v.shape[-1]')
    if v.shape[-1] != n:
        raise ValueError('expected the same number of eigenvalues as '
                         'eigenvectors')

    # get indices for each first pair of complex eigenvalues
    complex_mask = iscomplex(w)
    n_complex = complex_mask.sum(axis=-1)

    # check if all complex eigenvalues have conjugate pairs
    if not (n_complex % 2 == 0).all():
        raise ValueError('expected complex-conjugate pairs of eigenvalues')

    # find complex indices
    idx = nonzero(complex_mask)
    idx_stack = idx[:-1]
    idx_elem = idx[-1]

    # filter them to conjugate indices, assuming pairs are not interleaved
    j = idx_elem[0::2]
    k = idx_elem[1::2]
    stack_ind = ()
    for i in idx_stack:
        # should never happen, assuming nonzero orders by the last axis
        assert (i[0::2] == i[1::2]).all(), \
                "Conjugate pair spanned different arrays!"
        stack_ind += (i[0::2],)

    # all eigenvalues to diagonal form
    wr = zeros(M + (n, n), dtype=w.real.dtype)
    di = range(n)
    wr[..., di, di] = w.real

    # complex eigenvalues to real block diagonal form
    wr[stack_ind + (j, k)] = w[stack_ind + (j,)].imag
    wr[stack_ind + (k, j)] = w[stack_ind + (k,)].imag

    # compute real eigenvectors associated with real block diagonal eigenvalues
    u = zeros(M + (n, n), dtype=np.cdouble)
    u[..., di, di] = 1.0
    u[stack_ind + (j, j)] = 0.5j
    u[stack_ind + (j, k)] = 0.5
    u[stack_ind + (k, j)] = -0.5j
    u[stack_ind + (k, k)] = 0.5

    # multiply matrices v and u (equivalent to v @ u)
    vr = einsum('...ij,...jk->...ik', v, u).real

    return wr, vr

