
def polar(*args, **kwargs) -> list[Line2D]:
    """
    Make a polar plot.

    call signature::

      polar(theta, r, [fmt], **kwargs)

    This is a convenience wrapper around `.pyplot.plot`. It ensures that the
    current Axes is polar (or creates one if needed) and then passes all parameters
    to ``.pyplot.plot``.

    .. note::
        When making polar plots using the :ref:`pyplot API <pyplot_interface>`,
        ``polar()`` should typically be the first command because that makes sure
        a polar Axes is created. Using other commands such as ``plt.title()``
        before this can lead to the implicit creation of a rectangular Axes, in which
        case a subsequent ``polar()`` call will fail.
    """
    # If an axis already exists, check if it has a polar projection
    if gcf().get_axes():
        ax = gca()
        if not isinstance(ax, PolarAxes):
            _api.warn_deprecated(
                "3.10",
                message="There exists a non-polar current Axes. Therefore, the "
                        "resulting plot from 'polar()' is non-polar. You likely "
                        "should call 'polar()' before any other pyplot plotting "
                        "commands. "
                        "Support for this scenario is deprecated in %(since)s and "
                        "will raise an error in %(removal)s"
            )
    else:
        ax = axes(projection="polar")
    return ax.plot(*args, **kwargs)


def polar(abs: TensorLikeType, angle: TensorLikeType) -> TensorLikeType:
    result = torch.complex(abs, angle)
    result.real = abs * torch.cos(angle)
    result.imag = abs * torch.sin(angle)
    return result


def polar(a, side="right"):
    """
    Compute the polar decomposition.

    Returns the factors of the polar decomposition [1]_ `u` and `p` such
    that ``a = up`` (if `side` is "right") or ``a = pu`` (if `side` is
    "left"), where `p` is positive semidefinite. Depending on the shape
    of `a`, either the rows or columns of `u` are orthonormal. When `a`
    is a square array, `u` is a square unitary array. When `a` is not
    square, the "canonical polar decomposition" [2]_ is computed.

    Parameters
    ----------
    a : (m, n) array_like
        The array to be factored.
    side : {'left', 'right'}, optional
        Determines whether a right or left polar decomposition is computed.
        If `side` is "right", then ``a = up``.  If `side` is "left",  then
        ``a = pu``.  The default is "right".

    Returns
    -------
    u : (m, n) ndarray
        If `a` is square, then `u` is unitary. If m > n, then the columns
        of `u` are orthonormal, and if m < n, then the rows of `u` are
        orthonormal.
    p : ndarray
        `p` is Hermitian positive semidefinite. If `a` is nonsingular, `p`
        is positive definite. The shape of `p` is (n, n) or (m, m), depending
        on whether `side` is "right" or "left", respectively.

    References
    ----------
    .. [1] R. A. Horn and C. R. Johnson, "Matrix Analysis", Cambridge
           University Press, 1985.
    .. [2] N. J. Higham, "Functions of Matrices: Theory and Computation",
           SIAM, 2008.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import polar
    >>> a = np.array([[1, -1], [2, 4]])
    >>> u, p = polar(a)
    >>> u
    array([[ 0.85749293, -0.51449576],
           [ 0.51449576,  0.85749293]])
    >>> p
    array([[ 1.88648444,  1.2004901 ],
           [ 1.2004901 ,  3.94446746]])

    A non-square example, with m < n:

    >>> b = np.array([[0.5, 1, 2], [1.5, 3, 4]])
    >>> u, p = polar(b)
    >>> u
    array([[-0.21196618, -0.42393237,  0.88054056],
           [ 0.39378971,  0.78757942,  0.4739708 ]])
    >>> p
    array([[ 0.48470147,  0.96940295,  1.15122648],
           [ 0.96940295,  1.9388059 ,  2.30245295],
           [ 1.15122648,  2.30245295,  3.65696431]])
    >>> u.dot(p)   # Verify the decomposition.
    array([[ 0.5,  1. ,  2. ],
           [ 1.5,  3. ,  4. ]])
    >>> u.dot(u.T)   # The rows of u are orthonormal.
    array([[  1.00000000e+00,  -2.07353665e-17],
           [ -2.07353665e-17,   1.00000000e+00]])

    Another non-square example, with m > n:

    >>> c = b.T
    >>> u, p = polar(c)
    >>> u
    array([[-0.21196618,  0.39378971],
           [-0.42393237,  0.78757942],
           [ 0.88054056,  0.4739708 ]])
    >>> p
    array([[ 1.23116567,  1.93241587],
           [ 1.93241587,  4.84930602]])
    >>> u.dot(p)   # Verify the decomposition.
    array([[ 0.5,  1.5],
           [ 1. ,  3. ],
           [ 2. ,  4. ]])
    >>> u.T.dot(u)  # The columns of u are orthonormal.
    array([[  1.00000000e+00,  -1.26363763e-16],
           [ -1.26363763e-16,   1.00000000e+00]])

    """
    if side not in ['right', 'left']:
        raise ValueError("`side` must be either 'right' or 'left'")
    a = np.asarray(a)
    if a.ndim != 2:
        raise ValueError("`a` must be a 2-D array.")

    w, s, vh = svd(a, full_matrices=False)
    u = w.dot(vh)
    if side == 'right':
        # a = up
        p = (vh.T.conj() * s).dot(vh)
    else:
        # a = pu
        p = (w * s).dot(w.T.conj())
    return u, p


def polar(ctx, z):
    return (ctx.fabs(z), ctx.arg(z))


def polar(a: ArrayLike, side: str = 'right', *, method: str = 'qdwh', eps: float | None = None,
          max_iterations: int | None = None) -> tuple[Array, Array]:
  r"""Computes the polar decomposition.

  Given the :math:`m \times n` matrix :math:`a`, returns the factors of the polar
  decomposition :math:`u` (also :math:`m \times n`) and :math:`p` such that
  :math:`a = up` (if side is ``"right"``; :math:`p` is :math:`n \times n`) or
  :math:`a = pu` (if side is ``"left"``; :math:`p` is :math:`m \times m`),
  where :math:`p` is positive semidefinite.  If :math:`a` is nonsingular,
  :math:`p` is positive definite and the
  decomposition is unique. :math:`u` has orthonormal columns unless
  :math:`n > m`, in which case it has orthonormal rows.

  Writing the SVD of :math:`a` as
  :math:`a = u_\mathit{svd} \cdot s_\mathit{svd} \cdot v^h_\mathit{svd}`, we
  have :math:`u = u_\mathit{svd} \cdot v^h_\mathit{svd}`. Thus the unitary
  factor :math:`u` can be constructed as the application of the sign function to
  the singular values of :math:`a`; or, if :math:`a` is Hermitian, the
  eigenvalues.

  Several methods exist to compute the polar decomposition. Currently two
  are supported:

  * ``method="svd"``:

    Computes the SVD of :math:`a` and then forms
    :math:`u = u_\mathit{svd} \cdot v^h_\mathit{svd}`.

  * ``method="qdwh"``:

    Applies the `QDWH`_ (QR-based Dynamically Weighted Halley) algorithm.

  Args:
    a: array of shape ``(..., m, n)``.
    side: Determines whether a right or left polar decomposition is computed.
      If ``side`` is ``"right"`` then :math:`a = up`. If ``side`` is ``"left"``
      then :math:`a = pu`. The default is ``"right"``.
    method: Determines the algorithm used, as described above.
    precision: :class:`~jax.lax.Precision` object specifying the matmul precision.
    eps: The final result will satisfy
      :math:`\left|x_k - x_{k-1}\right| < \left|x_k\right| (4\epsilon)^{\frac{1}{3}}`,
      where :math:`x_k` are the QDWH iterates. Ignored if ``method`` is not
      ``"qdwh"``.
    max_iterations: Iterations will terminate after this many steps even if the
      above is unsatisfied.  Ignored if ``method`` is not ``"qdwh"``.

  Returns:
    A ``(unitary, posdef)`` tuple, where ``unitary`` is the unitary factor
    of shape ``(..., m, n)``, and ``posdef`` is the positive-semidefinite
    factor. ``posdef`` has shape ``(..., n, n)`` or ``(..., m, m)`` depending
    on whether ``side`` is ``"right"`` or ``"left"``, respectively.

  Examples:

    Polar decomposition of a 3x3 matrix:

    >>> a = jnp.array([[1., 2., 3.],
    ...                [5., 4., 2.],
    ...                [3., 2., 1.]])
    >>> U, P = jax.scipy.linalg.polar(a)

    U is a Unitary Matrix:

    >>> jnp.round(U.T @ U)  # doctest: +SKIP
    Array([[ 1., -0., -0.],
           [-0.,  1.,  0.],
           [-0.,  0.,  1.]], dtype=float32)

    P is positive-semidefinite Matrix:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(P)
    [[4.79 3.25 1.23]
     [3.25 3.06 2.01]
     [1.23 2.01 2.91]]

    The original matrix can be reconstructed by multiplying the U and P:

    >>> a_reconstructed = U @ P
    >>> jnp.allclose(a, a_reconstructed)
    Array(True, dtype=bool)

  .. _QDWH: https://epubs.siam.org/doi/abs/10.1137/090774999
  """
  arr = jnp.asarray(a)
  if arr.ndim < 2:
    raise ValueError("The input `a` must be at least a 2-D array.")

  if side not in ["right", "left"]:
    raise ValueError("The argument `side` must be either 'right' or 'left'.")

  sig = "(m,n)->(m,n),(n,n)" if side == "right" else "(m,n)->(m,n),(m,m)"
  return jnp_vectorize.vectorize(
      partial(_polar_2d, side=side, method=method, eps=eps,
              max_iterations=max_iterations),
      signature=sig)(arr)

