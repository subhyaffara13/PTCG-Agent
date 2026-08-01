
def outer(a: ArrayLike, b: ArrayLike, out: OutArray | None = None):
    return torch.outer(a, b)


def outer(g: jit_utils.GraphContext, input, other):
    # make sure to cast other to self's type
    if _type_utils.JitScalarType.from_value(
        other, _type_utils.JitScalarType.UNDEFINED
    ) != _type_utils.JitScalarType.from_value(input):
        other = g.op(
            "Cast",
            other,
            to_i=_type_utils.JitScalarType.from_value(input).onnx_type(),
        )
    return _einsum_helper(g, "i,j->ij", [input, other])


def outer(vec1, vec2):
    """Outer product convenience wrapper for Vector.outer():\n"""
    if not isinstance(vec1, Vector):
        raise TypeError('Outer product is between two Vectors')
    return vec1.outer(vec2)


def outer(x1: Array, x2: Array, /, xp: Namespace, **kwargs: object) -> Array:
    return xp.outer(x1, x2, **kwargs)


def outer(x1, x2, /):
    """
    Compute the outer product of two vectors.

    This function is Array API compatible. Compared to ``np.outer``
    it accepts 1-dimensional inputs only.

    Parameters
    ----------
    x1 : (M,) array_like
        One-dimensional input array of size ``N``.
        Must have a numeric data type.
    x2 : (N,) array_like
        One-dimensional input array of size ``M``.
        Must have a numeric data type.

    Returns
    -------
    out : (M, N) ndarray
        ``out[i, j] = a[i] * b[j]``

    See also
    --------
    outer

    Examples
    --------
    Make a (*very* coarse) grid for computing a Mandelbrot set:

    >>> rl = np.linalg.outer(np.ones((5,)), np.linspace(-2, 2, 5))
    >>> rl
    array([[-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.]])
    >>> im = np.linalg.outer(1j*np.linspace(2, -2, 5), np.ones((5,)))
    >>> im
    array([[0.+2.j, 0.+2.j, 0.+2.j, 0.+2.j, 0.+2.j],
           [0.+1.j, 0.+1.j, 0.+1.j, 0.+1.j, 0.+1.j],
           [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
           [0.-1.j, 0.-1.j, 0.-1.j, 0.-1.j, 0.-1.j],
           [0.-2.j, 0.-2.j, 0.-2.j, 0.-2.j, 0.-2.j]])
    >>> grid = rl + im
    >>> grid
    array([[-2.+2.j, -1.+2.j,  0.+2.j,  1.+2.j,  2.+2.j],
           [-2.+1.j, -1.+1.j,  0.+1.j,  1.+1.j,  2.+1.j],
           [-2.+0.j, -1.+0.j,  0.+0.j,  1.+0.j,  2.+0.j],
           [-2.-1.j, -1.-1.j,  0.-1.j,  1.-1.j,  2.-1.j],
           [-2.-2.j, -1.-2.j,  0.-2.j,  1.-2.j,  2.-2.j]])

    An example using a "vector" of letters:

    >>> x = np.array(['a', 'b', 'c'], dtype=np.object_)
    >>> np.linalg.outer(x, [1, 2, 3])
    array([['a', 'aa', 'aaa'],
           ['b', 'bb', 'bbb'],
           ['c', 'cc', 'ccc']], dtype=object)

    """
    x1 = asanyarray(x1)
    x2 = asanyarray(x2)
    if x1.ndim != 1 or x2.ndim != 1:
        raise ValueError(
            "Input arrays must be one-dimensional, but they are "
            f"{x1.ndim=} and {x2.ndim=}."
        )
    return _core_outer(x1, x2, out=None)


def outer(a, b):
    "maskedarray version of the numpy function."
    fa = filled(a, 0).ravel()
    fb = filled(b, 0).ravel()
    d = np.outer(fa, fb)
    ma = getmask(a)
    mb = getmask(b)
    if ma is nomask and mb is nomask:
        return masked_array(d)
    ma = getmaskarray(a)
    mb = getmaskarray(b)
    m = make_mask(1 - np.outer(1 - ma, 1 - mb), copy=False)
    return masked_array(d, mask=m)


def outer(a, b, out=None):
    """
    Compute the outer product of two vectors.

    Given two vectors `a` and `b` of length ``M`` and ``N``, respectively,
    the outer product [1]_ is::

      [[a_0*b_0  a_0*b_1 ... a_0*b_{N-1} ]
       [a_1*b_0    .
       [ ...          .
       [a_{M-1}*b_0            a_{M-1}*b_{N-1} ]]

    Parameters
    ----------
    a : (M,) array_like
        First input vector.  Input is flattened if
        not already 1-dimensional.
    b : (N,) array_like
        Second input vector.  Input is flattened if
        not already 1-dimensional.
    out : (M, N) ndarray, optional
        A location where the result is stored

    Returns
    -------
    out : (M, N) ndarray
        ``out[i, j] = a[i] * b[j]``

    See also
    --------
    inner
    einsum : ``einsum('i,j->ij', a.ravel(), b.ravel())`` is the equivalent.
    ufunc.outer : A generalization to dimensions other than 1D and other
                  operations. ``np.multiply.outer(a.ravel(), b.ravel())``
                  is the equivalent.
    linalg.outer : An Array API compatible variation of ``np.outer``,
                   which accepts 1-dimensional inputs only.
    tensordot : ``np.tensordot(a.ravel(), b.ravel(), axes=((), ()))``
                is the equivalent.

    References
    ----------
    .. [1] G. H. Golub and C. F. Van Loan, *Matrix Computations*, 3rd
           ed., Baltimore, MD, Johns Hopkins University Press, 1996,
           pg. 8.

    Examples
    --------
    Make a (*very* coarse) grid for computing a Mandelbrot set:

    >>> import numpy as np
    >>> rl = np.outer(np.ones((5,)), np.linspace(-2, 2, 5))
    >>> rl
    array([[-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.]])
    >>> im = np.outer(1j*np.linspace(2, -2, 5), np.ones((5,)))
    >>> im
    array([[0.+2.j, 0.+2.j, 0.+2.j, 0.+2.j, 0.+2.j],
           [0.+1.j, 0.+1.j, 0.+1.j, 0.+1.j, 0.+1.j],
           [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
           [0.-1.j, 0.-1.j, 0.-1.j, 0.-1.j, 0.-1.j],
           [0.-2.j, 0.-2.j, 0.-2.j, 0.-2.j, 0.-2.j]])
    >>> grid = rl + im
    >>> grid
    array([[-2.+2.j, -1.+2.j,  0.+2.j,  1.+2.j,  2.+2.j],
           [-2.+1.j, -1.+1.j,  0.+1.j,  1.+1.j,  2.+1.j],
           [-2.+0.j, -1.+0.j,  0.+0.j,  1.+0.j,  2.+0.j],
           [-2.-1.j, -1.-1.j,  0.-1.j,  1.-1.j,  2.-1.j],
           [-2.-2.j, -1.-2.j,  0.-2.j,  1.-2.j,  2.-2.j]])

    An example using a "vector" of letters:

    >>> x = np.array(['a', 'b', 'c'], dtype=np.object_)
    >>> np.outer(x, [1, 2, 3])
    array([['a', 'aa', 'aaa'],
           ['b', 'bb', 'bbb'],
           ['c', 'cc', 'ccc']], dtype=object)

    """
    a = asarray(a)
    b = asarray(b)
    return multiply(a.ravel()[:, newaxis], b.ravel()[newaxis, :], out)


def outer(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute the outer product of two 1-dimensional arrays.

  JAX implementation of :func:`numpy.linalg.outer`.

  Args:
    x1: array
    x2: array

  Returns:
    array containing the outer product of ``x1`` and ``x2``

  See also:
    :func:`jax.numpy.outer`: similar function in the main :mod:`jax.numpy` module.

  Examples:
    >>> x1 = jnp.array([1, 2, 3])
    >>> x2 = jnp.array([4, 5, 6])
    >>> jnp.linalg.outer(x1, x2)
    Array([[ 4,  5,  6],
           [ 8, 10, 12],
           [12, 15, 18]], dtype=int32)
  """
  x1, x2 = ensure_arraylike("jnp.linalg.outer", x1, x2)
  if x1.ndim != 1 or x2.ndim != 1:
    raise ValueError(f"Input arrays must be one-dimensional, but they are {x1.ndim=} {x2.ndim=}")
  return x1[:, None] * x2[None, :]


def outer(a: ArrayLike, b: ArrayLike, out: None = None) -> Array:
  """Compute the outer product of two arrays.

  JAX implementation of :func:`numpy.outer`.

  Args:
    a: first input array, if not 1D it will be flattened.
    b: second input array, if not 1D it will be flattened.
    out: unsupported by JAX.

  Returns:
    The outer product of the inputs ``a`` and ``b``. Returned array
    will be of shape ``(a.size, b.size)``.

  See also:
    - :func:`jax.numpy.inner`: compute the inner product of two arrays.
    - :func:`jax.numpy.einsum`: Einstein summation.

  Examples:
    >>> a = jnp.array([1, 2, 3])
    >>> b = jnp.array([4, 5, 6])
    >>> jnp.outer(a, b)
    Array([[ 4,  5,  6],
           [ 8, 10, 12],
           [12, 15, 18]], dtype=int32)
  """
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.outer is not supported.")
  a, b = util.ensure_arraylike("outer", a, b)
  a, b = util.promote_dtypes(a, b)
  return a.ravel()[:, None] * b.ravel()[None, :]

