from typing import Any, Callable

def schur(a, output='real', lwork=None, overwrite_a=False, sort=None,
          check_finite=True):
    """
    Compute Schur decomposition of a matrix.

    The Schur decomposition is::

        A = Z T Z^H

    where Z is unitary and T is either upper-triangular, or for real
    Schur decomposition (output='real'), quasi-upper triangular. In
    the quasi-triangular form, 2x2 blocks describing complex-valued
    eigenvalue pairs may extrude from the diagonal.

    Parameters
    ----------
    a : (M, M) array_like
        Matrix to decompose
    output : {'real', 'complex'}, optional
        When the dtype of `a` is real, this specifies whether to compute
        the real or complex Schur decomposition.
        When the dtype of `a` is complex, this argument is ignored, and the
        complex Schur decomposition is computed.
    lwork : int, optional
        Work array size. If None or -1, it is automatically computed.
    overwrite_a : bool, optional
        Whether to overwrite data in a (may improve performance).
        See :ref:`tutorial_linalg_overwrite` for details.
    sort : {None, callable, 'lhp', 'rhp', 'iuc', 'ouc'}, optional
        Specifies whether the upper eigenvalues should be sorted. A callable
        may be passed that, given an eigenvalue, returns a boolean denoting
        whether the eigenvalue should be sorted to the top-left (True).

        - If ``output='complex'`` OR the dtype of `a` is complex, the callable
          should have one argument: the eigenvalue expressed as a complex number.
        - If ``output='real'`` AND the dtype of `a` is real, the callable should have
          two arguments: the real and imaginary parts of the eigenvalue, respectively.

        Alternatively, string parameters may be used::

            'lhp'   Left-hand plane (real(eigenvalue) < 0.0)
            'rhp'   Right-hand plane (real(eigenvalue) >= 0.0)
            'iuc'   Inside the unit circle (abs(eigenvalue) <= 1.0)
            'ouc'   Outside the unit circle (abs(eigenvalue) > 1.0)

        Defaults to None (no sorting).
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    T : (M, M) ndarray
        Schur form of A. It is real-valued for the real Schur decomposition.
    Z : (M, M) ndarray
        A unitary Schur transformation matrix for A.
        It is real-valued for the real Schur decomposition.
    sdim : int
        If and only if sorting was requested, a third return value will
        contain the number of eigenvalues satisfying the sort condition.
        Note that complex conjugate pairs for which the condition is true
        for either eigenvalue count as 2.

    Raises
    ------
    LinAlgError
        Error raised under three conditions:

        1. The algorithm failed due to a failure of the QR algorithm to
           compute all eigenvalues.
        2. If eigenvalue sorting was requested, the eigenvalues could not be
           reordered due to a failure to separate eigenvalues, usually because
           of poor conditioning.
        3. If eigenvalue sorting was requested, roundoff errors caused the
           leading eigenvalues to no longer satisfy the sorting condition.

    See Also
    --------
    rsf2csf : Convert real Schur form to complex Schur form

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import schur, eigvals
    >>> A = np.array([[0, 2, 2], [0, 1, 2], [1, 0, 1]])
    >>> T, Z = schur(A)
    >>> T
    array([[ 2.65896708,  1.42440458, -1.92933439],
           [ 0.        , -0.32948354, -0.49063704],
           [ 0.        ,  1.31178921, -0.32948354]])
    >>> Z
    array([[0.72711591, -0.60156188, 0.33079564],
           [0.52839428, 0.79801892, 0.28976765],
           [0.43829436, 0.03590414, -0.89811411]])

    >>> T2, Z2 = schur(A, output='complex')
    >>> T2
    array([[ 2.65896708, -1.22839825+1.32378589j,  0.42590089+1.51937378j], # may vary
           [ 0.        , -0.32948354+0.80225456j, -0.59877807+0.56192146j],
           [ 0.        ,  0.                    , -0.32948354-0.80225456j]])
    >>> eigvals(T2)
    array([2.65896708, -0.32948354+0.80225456j, -0.32948354-0.80225456j])   # may vary

    A custom eigenvalue-sorting condition that sorts by positive imaginary part
    is satisfied by only one eigenvalue.

    >>> _, _, sdim = schur(A, output='complex', sort=lambda x: x.imag > 1e-15)
    >>> sdim
    1

    When ``output='real'`` and the array `a` is real, the `sort` callable must accept
    the real and imaginary parts as separate arguments. Note that now the complex
    eigenvalues ``-0.32948354+0.80225456j`` and ``-0.32948354-0.80225456j`` will be
    treated as a complex conjugate pair, and according to the `sdim` documentation,
    complex conjugate pairs for which the condition is True for *either* eigenvalue
    increase `sdim` by *two*.

    >>> _, _, sdim = schur(A, output='real', sort=lambda x, y: y > 1e-15)
    >>> sdim
    2

    """
    if output not in ['real', 'complex', 'r', 'c']:
        raise ValueError("argument must be 'real', or 'complex'")
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if np.issubdtype(a1.dtype, np.integer):
        a1 = asarray(a, dtype=np.dtype("long"))
    if len(a1.shape) != 2 or (a1.shape[0] != a1.shape[1]):
        raise ValueError('expected square matrix')

    typ = a1.dtype.char
    if output in ['complex', 'c'] and typ not in ['F', 'D']:
        if typ in _double_precision:
            a1 = a1.astype('D')
        else:
            a1 = a1.astype('F')

    # accommodate empty matrix
    if a1.size == 0:
        t0, z0 = schur(np.eye(2, dtype=a1.dtype))
        if sort is None:
            return (np.empty_like(a1, dtype=t0.dtype),
                    np.empty_like(a1, dtype=z0.dtype))
        else:
            return (np.empty_like(a1, dtype=t0.dtype),
                    np.empty_like(a1, dtype=z0.dtype), 0)

    overwrite_a = overwrite_a or (_datacopied(a1, a))
    gees, = get_lapack_funcs(('gees',), (a1,))
    if lwork is None or lwork == -1:
        # get optimal work array
        result = gees(lambda x: None, a1, lwork=-1)
        lwork = result[-2][0].real.astype(np.int_)

    if sort is None:
        sort_t = 0
        def sfunction(x, y=None):
            return None
    else:
        sort_t = 1
        if callable(sort):
            sfunction = sort
        elif sort == 'lhp':
            def sfunction(x, y=None):
                return x.real < 0.0
        elif sort == 'rhp':
            def sfunction(x, y=None):
                return x.real >= 0.0
        elif sort == 'iuc':
            def sfunction(x, y=None):
                z = x if y is None else x + y*1j
                return abs(z) <= 1.0
        elif sort == 'ouc':
            def sfunction(x, y=None):
                z = x if y is None else x + y*1j
                return abs(z) > 1.0
        else:
            raise ValueError("'sort' parameter must either be 'None', or a "
                             "callable, or one of ('lhp','rhp','iuc','ouc')")

    result = gees(sfunction, a1, lwork=lwork, overwrite_a=overwrite_a,
                  sort_t=sort_t)

    info = result[-1]
    if info < 0:
        raise ValueError(f'illegal value in {-info}-th argument of internal gees')
    elif info == a1.shape[0] + 1:
        raise LinAlgError('Eigenvalues could not be separated for reordering.')
    elif info == a1.shape[0] + 2:
        raise LinAlgError('Leading eigenvalues do not satisfy sort condition.')
    elif info > 0:
        raise LinAlgError("Schur form not found. Possibly ill-conditioned.")

    if sort is None:
        return result[0], result[-3]
    else:
        return result[0], result[-3], result[1]


def schur(ctx, A, overwrite_a = False):
    """
    This routine computes the Schur decomposition of a square matrix A.
    Given A, an unitary matrix Q is determined such that

          Q' A Q = R                and               Q' Q = Q Q' = 1

    where R is an upper right triangular matrix. Here ' denotes the
    hermitian transpose (i.e. transposition and conjugation).

    input:
      A            : a real or complex square matrix
      overwrite_a  : if true, allows modification of A which may improve
                     performance. if false, A is not modified.

    output:
      Q : an unitary matrix
      R : an upper right triangular matrix

    return value:   (Q, R)

    example:
      >>> from mpmath import mp
      >>> A = mp.matrix([[3, -1, 2], [2, 5, -5], [-2, -3, 7]])
      >>> Q, R = mp.schur(A)
      >>> mp.nprint(R, 3) # doctest:+SKIP
      [2.0  0.417  -2.53]
      [0.0    4.0  -4.74]
      [0.0    0.0    9.0]
      >>> print(mp.chop(A - Q * R * Q.transpose_conj()))
      [0.0  0.0  0.0]
      [0.0  0.0  0.0]
      [0.0  0.0  0.0]

    warning: The Schur decomposition is not unique.
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
        for y in xrange(x + 2, n):
            A[y,x] = 0

    hessenberg_qr(ctx, A, Q)

    return Q, A


def schur(
    x: ArrayLike,
    *,
    compute_schur_vectors: bool = True,
    sort_eig_vals: bool = False,
    select_callable: Callable[..., Any] | None = None,
) -> tuple[Array, Array]:
  r"""Schur decomposition.

  Only implemented on CPU.

  Computes the Schur decomposition:

  .. math::
    A = Q \, U \, Q^{-H}

  for a square matrix :math:`A`.

  Args:
    x: A batch of square matrices with shape ``[..., m, m]``.
    compute_schur_vectors: If ``True``, compute the Schur vectors ::math:`Q`,
      otherwise only :math:`U` is computed.
    sort_eig_vals: Unused.
    select_callable: Unused.

  Returns:
    A pair of arrays ``U, Q``, if ``compute_schur_vectors=True``, otherwise
    only ``U`` is returned.
  """
  return schur_p.bind(
      x,
      compute_schur_vectors=compute_schur_vectors,
      sort_eig_vals=sort_eig_vals,
      select_callable=select_callable)


def schur(a: ArrayLike, output: str = 'real') -> tuple[Array, Array]:
  """Compute the Schur decomposition

  Only implemented on CPU.

  JAX implementation of :func:`scipy.linalg.schur`.

  The Schur form `T` of a matrix `A` satisfies:

  .. math::

     A = Z T Z^H

  where `Z` is unitary, and `T` is upper-triangular for the complex-valued Schur
  decomposition (i.e. ``output="complex"``) and is quasi-upper-triangular for the
  real-valued Schur decomposition (i.e. ``output="real"``). In the quasi-triangular
  case, the diagonal may include 2x2 blocks associated with complex-valued
  eigenvalue pairs of `A`.

  Args:
    a: input array of shape ``(..., N, N)``
    output: Specify whether to compute the ``"real"`` (default) or ``"complex"``
      Schur decomposition.

  Returns:
    A tuple of arrays ``(T, Z)``

    - ``T`` is a shape ``(..., N, N)`` array containing the upper-triangular
      Schur form of the input.
    - ``Z`` is a shape ``(..., N, N)`` array containing the unitary Schur
      transformation matrix.

  See also:
    - :func:`jax.scipy.linalg.rsf2csf`: convert real Schur form to complex Schur form.
    - :func:`jax.lax.linalg.schur`: XLA-style API for Schur decomposition.

  Examples:
    A Schur decomposition of a 3x3 matrix:

    >>> a = jnp.array([[1., 2., 3.],
    ...                [1., 4., 2.],
    ...                [3., 2., 1.]])
    >>> T, Z = jax.scipy.linalg.schur(a)

    The Schur form ``T`` is quasi-upper-triangular in general, but is truly
    upper-triangular in this case because the input matrix is symmetric:

    >>> T  # doctest: +SKIP
    Array([[-2.0000005 ,  0.5066295 , -0.43360388],
           [ 0.        ,  1.5505103 ,  0.74519426],
           [ 0.        ,  0.        ,  6.449491  ]], dtype=float32)

    The transformation matrix ``Z`` is unitary:

    >>> jnp.allclose(Z.T @ Z, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    The input can be reconstructed from the outputs:

    >>> jnp.allclose(Z @ T @ Z.T, a)
    Array(True, dtype=bool)
  """
  if output not in ('real', 'complex'):
    raise ValueError(
      f"Expected 'output' to be either 'real' or 'complex', got {output=}.")
  return _schur(a, output)

