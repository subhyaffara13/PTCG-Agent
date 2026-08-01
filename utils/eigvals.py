
def eigvals(a: ArrayLike):
    a = _atleast_float_1(a)
    result = torch.linalg.eigvals(a)
    if not a.is_complex() and result.is_complex() and (result.imag == 0).all():
        result = result.real
    return result


def eigvals(a, b=None, overwrite_a=False, overwrite_b=False, check_finite=True,
            homogeneous_eigvals=False):
    r"""
    Compute eigenvalues from an ordinary or generalized eigenvalue problem.

    Find eigenvalues, ``w``, of a general matrix::

        a @ vr[:, i] = w[i] * b  @ vr[:, i]

    Parameters
    ----------
    a : (..., M, M) array_like
        A complex or real matrix (or a stack of matrices), whose eigenvalues will be
        computed.
    b : (..., M, M) array_like, optional
        Right-hand side matrix (or a stack of matrices) in a generalized eigenvalue
        problem. If omitted (default), identity matrix is assumed.
    overwrite_a : bool, optional
        Whether to overwrite data in a (may improve performance). Default is False.
    overwrite_b : bool, optional
        Whether to overwrite data in b (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities
        or NaNs.
    homogeneous_eigvals : bool, optional
        If True, return the eigenvalues in homogeneous coordinates.
        In this case ``w`` is a ``(2, M)`` array so that::

            w[1, i] * a @ vr[:, i] = w[0, i] * b @ vr[:, i]

        This option is sometimes useful for generalized eigenvalue problems,
        ``b is not None``, where an eigenvalue, :math:`\lambda = \alpha / \beta`,
        can over- or underflow; typically, :\math:`\alpha` and :math:`\beta` are of the
        order of ``norm(a)`` and ``norm(b)``, respectively.

        Default is False.

    Returns
    -------
    w : (..., M,) or (..., 2, M) complex ndarray
        The eigenvalues, each repeated according to its multiplicity
        but not in any specific order. The shape is ``(..., M)`` unless
        ``homogeneous_eigvals=True``.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge

    See Also
    --------
    eig : eigenvalues and right eigenvectors of general arrays.
    eigvalsh : eigenvalues of symmetric or Hermitian arrays
    eigvals_banded : eigenvalues for symmetric/Hermitian band matrices
    eigvalsh_tridiagonal : eigenvalues of symmetric/Hermitian tridiagonal
        matrices

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> a = np.array([[0., -1.],
    ...               [1.,  0.]])

    Compute the eigenvalues (``eigvals`` is the same as ``eig(a, right=False)``)

    >>> linalg.eigvals(a)
    array([0.+1.j, 0.-1.j])

    Solve a generalized eigenvalue problem:

    >>> b = np.array([[0., 1.], [1., 1.]])
    >>> linalg.eigvals(a, b)
    array([ 1.+0.j, -1.+0.j])

    Inputs with ``ndim > 2`` are interpreted as a batch of matrices

    >>> a2 = np.stack((a, 2*a))
    >>> linalg.eigvals(a2)
    array([[0.+1.j, 0.-1.j],
           [0.+2.j, 0.-2.j]])

    ``homogeneous_eigvals=True`` argument effectively separates each eigenvalue into a
    numerator-denominator pair:

    >>> a = np.array([[3., 0., 0.],
    ...               [0., 8., 0.],
    ...               [0., 0., 7.]])
    >>> b = 2*np.eye(3)
    >>> linalg.eigvals(a, b, homogeneous_eigvals=True)
    array([[3.+0.j, 8.+0.j, 7.+0.j],
           [2.+0.j, 2.+0.j, 2.+0.j]])
    """
    return eig(a, b=b, left=0, right=0, overwrite_a=overwrite_a,
                overwrite_b=overwrite_b, check_finite=check_finite,
                homogeneous_eigvals=homogeneous_eigvals)


def eigvals(x: Array, /) -> Array:
    try:
        from numpy.linalg._linalg import (  # type: ignore[attr-defined]
            _assert_stacked_square,
            _assert_finite,
            _commonType,
            _makearray,
            _raise_linalgerror_eigenvalues_nonconvergence,
            isComplexType,
            _complexType,
        )
    except ImportError:
        from numpy.linalg.linalg import (  # type: ignore[attr-defined]
            _assert_stacked_square,
            _assert_finite,
            _commonType,
            _makearray,
            _raise_linalgerror_eigenvalues_nonconvergence,
            isComplexType,
            _complexType,
        )
    from numpy.linalg import _umath_linalg

    x, wrap = _makearray(x)
    _assert_stacked_square(x)
    _assert_finite(x)
    t, result_t = _commonType(x)

    signature = 'D->D' if isComplexType(t) else 'd->D'
    with np.errstate(call=_raise_linalgerror_eigenvalues_nonconvergence,
                  invalid='call', over='ignore', divide='ignore',
                  under='ignore'):
        w = _umath_linalg.eigvals(x, signature=signature)

    result_t = _complexType(result_t)
    return w.astype(result_t, copy=False)


def eigvals(a):
    """
    Compute the eigenvalues of a general matrix.

    Main difference between `eigvals` and `eig`: the eigenvectors aren't
    returned.

    Parameters
    ----------
    a : (..., M, M) array_like
        A complex- or real-valued matrix whose eigenvalues will be computed.

    Returns
    -------
    w : (..., M,) ndarray
        The eigenvalues, each repeated according to its multiplicity.
        They are not necessarily ordered, nor are they necessarily
        real for real matrices.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eig : eigenvalues and right eigenvectors of general arrays
    eigvalsh : eigenvalues of real symmetric or complex Hermitian
               (conjugate symmetric) arrays.
    eigh : eigenvalues and eigenvectors of real symmetric or complex
           Hermitian (conjugate symmetric) arrays.
    scipy.linalg.eigvals : Similar function in SciPy.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    This is implemented using the ``_geev`` LAPACK routines which compute
    the eigenvalues and eigenvectors of general square arrays.

    Examples
    --------
    Illustration, using the fact that the eigenvalues of a diagonal matrix
    are its diagonal elements, that multiplying a matrix on the left
    by an orthogonal matrix, `Q`, and on the right by `Q.T` (the transpose
    of `Q`), preserves the eigenvalues of the "middle" matrix. In other words,
    if `Q` is orthogonal, then ``Q * A * Q.T`` has the same eigenvalues as
    ``A``:

    >>> import numpy as np
    >>> from numpy import linalg as LA
    >>> x = np.random.random()
    >>> Q = np.array([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])
    >>> LA.norm(Q[0, :]), LA.norm(Q[1, :]), np.dot(Q[0, :],Q[1, :])
    (1.0, 1.0, 0.0)

    Now multiply a diagonal matrix by ``Q`` on one side and
    by ``Q.T`` on the other:

    >>> D = np.diag((-1,1))
    >>> LA.eigvals(D)
    array([-1. + 0.j,  1. + 0.j])
    >>> A = np.dot(Q, D)
    >>> A = np.dot(A, Q.T)
    >>> LA.eigvals(A)
    array([ 1., -1.])  # random

    """
    a, wrap = _makearray(a)
    _assert_stacked_square(a)
    _assert_finite(a)
    t, result_t = _commonType(a)

    signature = 'D->D' if isComplexType(t) else 'd->D'
    with errstate(call=_raise_linalgerror_eigenvalues_nonconvergence,
                  invalid='call', over='ignore', divide='ignore',
                  under='ignore'):
        w = _umath_linalg.eigvals(a, signature=signature)

    return w.astype(_complexType(result_t), copy=False)


def eigvals(a: ArrayLike) -> Array:
  """
  Compute the eigenvalues of a general matrix.

  JAX implementation of :func:`numpy.linalg.eigvals`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the eigenvalues.

  Returns:
    An array of shape ``(..., M)`` containing the eigenvalues.

  See also:
    - :func:`jax.numpy.linalg.eig`: computes eigenvalues eigenvectors of a general matrix.
    - :func:`jax.numpy.linalg.eigh`: computes eigenvalues eigenvectors of a Hermitian matrix.

  Notes:
    - This differs from :func:`numpy.linalg.eigvals` in that the return type of
      :func:`jax.numpy.linalg.eigvals` is always complex64 for 32-bit input, and
      complex128 for 64-bit input.
    - At present, non-symmetric eigendecomposition is only implemented on the CPU backend.

  Examples:
    >>> a = jnp.array([[1., 2.],
    ...                [2., 1.]])
    >>> w = jnp.linalg.eigvals(a)
    >>> with jnp.printoptions(precision=2):
    ...  w
    Array([ 3.+0.j, -1.+0.j], dtype=complex64)
  """
  a = ensure_arraylike("jnp.linalg.eigvals", a)
  a, = promote_dtypes_inexact(a)
  return lax_linalg.eig(a, compute_left_eigenvectors=False,
                        compute_right_eigenvectors=False)[0]

