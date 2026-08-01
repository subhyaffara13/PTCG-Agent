
def hessenberg(a, calc_q=False, overwrite_a=False, check_finite=True):
    """
    Compute Hessenberg form of a matrix.

    The Hessenberg decomposition is::

        A = Q H Q^H

    where `Q` is unitary/orthogonal and `H` has only zero elements below
    the first sub-diagonal.

    Parameters
    ----------
    a : (M, M) array_like
        Matrix to bring into Hessenberg form.
    calc_q : bool, optional
        Whether to compute the transformation matrix.  Default is False.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance. Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    H : (M, M) ndarray
        Hessenberg form of `a`.
    Q : (M, M) ndarray
        Unitary/orthogonal similarity transformation matrix ``A = Q H Q^H``.
        Only returned if ``calc_q=True``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import hessenberg
    >>> A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])
    >>> H, Q = hessenberg(A, calc_q=True)
    >>> H
    array([[  2.        , -11.65843866,   1.42005301,   0.25349066],
           [ -9.94987437,  14.53535354,  -5.31022304,   2.43081618],
           [  0.        ,  -1.83299243,   0.38969961,  -0.51527034],
           [  0.        ,   0.        ,  -3.83189513,   1.07494686]])
    >>> np.allclose(Q @ H @ Q.conj().T - A, np.zeros((4, 4)))
    True
    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or (a1.shape[0] != a1.shape[1]):
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))

    if a1.size == 0:
        h3 = hessenberg(np.eye(3, dtype=a1.dtype))
        h = np.empty(a1.shape, dtype=h3.dtype)
        if not calc_q:
            return h
        else:
            h3, q3 = hessenberg(np.eye(3, dtype=a1.dtype), calc_q=True)
            q = np.empty(a1.shape, dtype=q3.dtype)
            h = np.empty(a1.shape, dtype=h3.dtype)
            return h, q

    # if 2x2 or smaller: already in Hessenberg
    if a1.shape[0] <= 2:
        if calc_q:
            return a1, eye(a1.shape[0])
        return a1

    gehrd, gebal, gehrd_lwork = get_lapack_funcs(('gehrd', 'gebal',
                                                  'gehrd_lwork'), (a1,))
    ba, lo, hi, pivscale, info = gebal(a1, permute=0, overwrite_a=overwrite_a)
    _check_info(info, 'gebal (hessenberg)', positive=False)
    n = len(a1)

    lwork = _compute_lwork(gehrd_lwork, ba.shape[0], lo=lo, hi=hi)

    hq, tau, info = gehrd(ba, lo=lo, hi=hi, lwork=lwork, overwrite_a=1)
    _check_info(info, 'gehrd (hessenberg)', positive=False)
    h = np.triu(hq, -1)
    if not calc_q:
        return h

    # use orghr/unghr to compute q
    orghr, orghr_lwork = get_lapack_funcs(('orghr', 'orghr_lwork'), (a1,))
    lwork = _compute_lwork(orghr_lwork, n, lo=lo, hi=hi)

    q, info = orghr(a=hq, tau=tau, lo=lo, hi=hi, lwork=lwork, overwrite_a=1)
    _check_info(info, 'orghr (hessenberg)', positive=False)
    return h, q


def hessenberg(ctx, A, overwrite_a = False):
    """
    This routine computes the Hessenberg decomposition of a square matrix A.
    Given A, an unitary matrix Q is determined such that

          Q' A Q = H                and               Q' Q = Q Q' = 1

    where H is an upper right Hessenberg matrix. Here ' denotes the hermitian
    transpose (i.e. transposition and conjugation).

    input:
      A            : a real or complex square matrix
      overwrite_a  : if true, allows modification of A which may improve
                     performance. if false, A is not modified.

    output:
      Q : an unitary matrix
      H : an upper right Hessenberg matrix

    example:
      >>> from mpmath import mp
      >>> A = mp.matrix([[3, -1, 2], [2, 5, -5], [-2, -3, 7]])
      >>> Q, H = mp.hessenberg(A)
      >>> mp.nprint(H, 3) # doctest:+SKIP
      [  3.15  2.23  4.44]
      [-0.769  4.85  3.05]
      [   0.0  3.61   7.0]
      >>> print(mp.chop(A - Q * H * Q.transpose_conj()))
      [0.0  0.0  0.0]
      [0.0  0.0  0.0]
      [0.0  0.0  0.0]

    return value:   (Q, H)
    """

    n = A.rows

    if n == 1:
        return (ctx.matrix([[1]]), A)

    if not overwrite_a:
        A = A.copy()

    T = ctx.matrix(n, 1)

    hessenberg_reduce_0(ctx, A, T)
    Q = A.copy()
    hessenberg_reduce_1(ctx, Q, T)

    for x in xrange(n):
        for y in xrange(x+2, n):
            A[y,x] = 0

    return Q, A


def hessenberg(a: ArrayLike) -> tuple[Array, Array]:
  """Reduces a square matrix to upper Hessenberg form.

  Currently implemented on CPU only.

  Args:
    a: A floating point or complex square matrix or batch of matrices.

  Returns:
    A ``(a, taus)`` pair, where the upper triangle and first subdiagonal of
    ``a`` contain the upper Hessenberg matrix, and the elements below the first
    subdiagonal contain the Householder reflectors. For each Householder
    reflector ``taus`` contains the scalar factors of the elementary Householder
    reflectors.
  """
  return hessenberg_p.bind(a)


def hessenberg(a: ArrayLike, *, calc_q: Literal[False], overwrite_a: bool = False,
               check_finite: bool = True) -> Array: ...


def hessenberg(a: ArrayLike, *, calc_q: Literal[True], overwrite_a: bool = False,
               check_finite: bool = True) -> tuple[Array, Array]: ...


def hessenberg(a: ArrayLike, *, calc_q: bool = False, overwrite_a: bool = False,
               check_finite: bool = True) -> Array | tuple[Array, Array]:
  """Compute the Hessenberg form of the matrix

  JAX implementation of :func:`scipy.linalg.hessenberg`.

  The Hessenberg form `H` of a matrix `A` satisfies:

  .. math::

     A = Q H Q^H

  where `Q` is unitary and `H` is zero below the first subdiagonal.

  Args:
    a : array of shape ``(..., N, N)``
    calc_q: if True, calculate the ``Q`` matrix (default: False)
    overwrite_a: unused by JAX
    check_finite: unused by JAX

  Returns:
    A tuple of arrays ``(H, Q)`` if ``calc_q`` is True, else an array ``H``

    - ``H`` has shape ``(..., N, N)`` and is the Hessenberg form of ``a``
    - ``Q`` has shape ``(..., N, N)`` and is the associated unitary matrix

  Examples:
    Computing the Hessenberg form of a 4x4 matrix

    >>> a = jnp.array([[1., 2., 3., 4.],
    ...                [1., 4., 2., 3.],
    ...                [3., 2., 1., 4.],
    ...                [2., 3., 2., 2.]])
    >>> H, Q = jax.scipy.linalg.hessenberg(a, calc_q=True)
    >>> with jnp.printoptions(suppress=True, precision=3):
    ...   print(H)
    [[ 1.    -5.078  1.167  1.361]
     [-3.742  5.786 -3.613 -1.825]
     [ 0.    -2.992  2.493 -0.577]
     [ 0.     0.    -0.043 -1.279]]

    Notice the zeros in the subdiagonal positions. The original matrix
    can be reconstructed using the ``Q`` vectors:

    >>> a_reconstructed = Q @ H @ Q.conj().T
    >>> jnp.allclose(a_reconstructed, a)
    Array(True, dtype=bool)
  """
  del overwrite_a, check_finite  # unused
  n = np.shape(a)[-1]
  if n == 0:
    if calc_q:
      return jnp.zeros_like(a), jnp.zeros_like(a)
    else:
      return jnp.zeros_like(a)
  a_out, taus = lax_linalg.hessenberg(a)
  h = jnp.triu(a_out, -1)
  if calc_q:
    q = lax_linalg.householder_product(a_out[..., 1:, :-1], taus)
    batch_dims = a_out.shape[:-2]
    q = jnp.block([[jnp.ones(batch_dims + (1, 1), dtype=a_out.dtype),
                    jnp.zeros(batch_dims + (1, n - 1), dtype=a_out.dtype)],
                   [jnp.zeros(batch_dims + (n - 1, 1), dtype=a_out.dtype), q]])
    return h, q
  else:
    return h

