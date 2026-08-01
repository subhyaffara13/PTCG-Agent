
def cross(a: ArrayLike, b: ArrayLike, axisa=-1, axisb=-1, axisc=-1, axis=None):
    # implementation vendored from
    # https://github.com/numpy/numpy/blob/v1.24.0/numpy/core/numeric.py#L1486-L1685
    if axis is not None:
        axisa, axisb, axisc = (axis,) * 3

    # Check axisa and axisb are within bounds
    axisa = _util.normalize_axis_index(axisa, a.ndim)
    axisb = _util.normalize_axis_index(axisb, b.ndim)

    # Move working axis to the end of the shape
    a = torch.moveaxis(a, axisa, -1)
    b = torch.moveaxis(b, axisb, -1)
    msg = "incompatible dimensions for cross product\n(dimension must be 2 or 3)"
    if a.shape[-1] not in (2, 3) or b.shape[-1] not in (2, 3):
        raise ValueError(msg)

    # Create the output array
    shape = broadcast_shapes(a[..., 0].shape, b[..., 0].shape)
    if a.shape[-1] == 3 or b.shape[-1] == 3:
        shape += (3,)
        # Check axisc is within bounds
        axisc = _util.normalize_axis_index(axisc, len(shape))
    dtype = _dtypes_impl.result_type_impl(a, b)
    cp = torch.empty(shape, dtype=dtype)

    # recast arrays as dtype
    a = _util.cast_if_needed(a, dtype)
    b = _util.cast_if_needed(b, dtype)

    # create local aliases for readability
    a0 = a[..., 0]
    a1 = a[..., 1]
    if a.shape[-1] == 3:
        a2 = a[..., 2]
    b0 = b[..., 0]
    b1 = b[..., 1]
    if b.shape[-1] == 3:
        b2 = b[..., 2]
    if cp.ndim != 0 and cp.shape[-1] == 3:
        cp0 = cp[..., 0]
        cp1 = cp[..., 1]
        cp2 = cp[..., 2]

    if a.shape[-1] == 2:
        if b.shape[-1] == 2:
            # a0 * b1 - a1 * b0
            cp[...] = a0 * b1 - a1 * b0
            return cp
        else:
            if b.shape[-1] != 3:
                raise AssertionError(f"b.shape[-1] must be 3, got {b.shape[-1]}")
            # cp0 = a1 * b2 - 0  (a2 = 0)
            # cp1 = 0 - a0 * b2  (a2 = 0)
            # cp2 = a0 * b1 - a1 * b0
            cp0[...] = a1 * b2
            cp1[...] = -a0 * b2
            cp2[...] = a0 * b1 - a1 * b0
    else:
        if a.shape[-1] != 3:
            raise AssertionError(f"a.shape[-1] must be 3, got {a.shape[-1]}")
        if b.shape[-1] == 3:
            cp0[...] = a1 * b2 - a2 * b1
            cp1[...] = a2 * b0 - a0 * b2
            cp2[...] = a0 * b1 - a1 * b0
        else:
            if b.shape[-1] != 2:
                raise AssertionError(f"b.shape[-1] must be 2, got {b.shape[-1]}")
            cp0[...] = -a2 * b1
            cp1[...] = a2 * b0
            cp2[...] = a0 * b1 - a1 * b0

    return torch.moveaxis(cp, -1, axisc)


def cross(a: Tensor, b: Tensor, dim: int = -1):
    torch._check(
        a.ndim == b.ndim,
        lambda: "linalg.cross: inputs must have the same number of dimensions.",
    )
    torch._check(
        a.size(dim) == 3 and b.size(dim) == 3,
        lambda: f"linalg.cross: inputs dim {dim} must have length 3, got {a.size(dim)} and {b.size(dim)}",
    )
    a, b = torch.broadcast_tensors(a, b)
    dim = utils.canonicalize_dim(a.ndim, dim)
    idx = torch.arange(3, device=a.device)
    return a.index_select(dim, (idx + 1) % 3) * b.index_select(
        dim, (idx + 2) % 3
    ) - a.index_select(dim, (idx + 2) % 3) * b.index_select(dim, (idx + 1) % 3)


def cross(g: jit_utils.GraphContext, input, other, dim=None):
    dim = symbolic_helper._get_dim_for_cross(input, dim)
    # If we have two tensors such that
    # A = [a, b, c], B = [d, e, f], we permute the tensor such that we have
    # After first roll,
    # A' = [b, c, a], B' = [f, d, e], so that we calculate (b*f, c*d, a*e)
    roll_x_1 = roll(g, input, [2], [dim])
    roll_y_1 = roll(g, other, [1], [dim])
    # After second roll,
    # A' = [c, a, b], B' = [e, f, d], so that we calculate (c*e, a*f, b*d)
    roll_x_2 = roll(g, input, [1], [dim])
    roll_y_2 = roll(g, other, [2], [dim])
    # cross product is calculated as
    # result = [(b*f - c*e), (c*d - a*f), (a*e - b*d)]
    return sub(g, mul(g, roll_x_1, roll_y_1), mul(g, roll_x_2, roll_y_2))


def cross(vect1, vect2):
    """
    Returns cross product of two vectors.

    Examples
    ========

    >>> from sympy.vector import CoordSys3D
    >>> from sympy.vector.vector import cross
    >>> R = CoordSys3D('R')
    >>> v1 = R.i + R.j + R.k
    >>> v2 = R.x * R.i + R.y * R.j + R.z * R.k
    >>> cross(v1, v2)
    (-R.y + R.z)*R.i + (R.x - R.z)*R.j + (-R.x + R.y)*R.k

    """
    if isinstance(vect1, Add):
        return VectorAdd.fromiter(cross(i, vect2) for i in vect1.args)
    if isinstance(vect2, Add):
        return VectorAdd.fromiter(cross(vect1, i) for i in vect2.args)
    if isinstance(vect1, BaseVector) and isinstance(vect2, BaseVector):
        if vect1._sys == vect2._sys:
            n1 = vect1.args[0]
            n2 = vect2.args[0]
            if n1 == n2:
                return Vector.zero
            n3 = ({0,1,2}.difference({n1, n2})).pop()
            sign = 1 if ((n1 + 1) % 3 == n2) else -1
            return sign*vect1._sys.base_vectors()[n3]
        from .functions import express
        try:
            v = express(vect1, vect2._sys)
        except ValueError:
            return Cross(vect1, vect2)
        else:
            return cross(v, vect2)
    if isinstance(vect1, VectorZero) or isinstance(vect2, VectorZero):
        return Vector.zero
    if isinstance(vect1, VectorMul):
        v1, m1 = next(iter(vect1.components.items()))
        return m1*cross(v1, vect2)
    if isinstance(vect2, VectorMul):
        v2, m2 = next(iter(vect2.components.items()))
        return m2*cross(vect1, v2)

    return Cross(vect1, vect2)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def cross(vec1, vec2):
    """Cross product convenience wrapper for Vector.cross(): \n"""
    if not isinstance(vec1, (Vector, Dyadic)):
        raise TypeError('Cross product is between two vectors')
    return vec1 ^ vec2


def cross(
    x1: Array,
    x2: Array,
    /,
    xp: Namespace,
    *,
    axis: int = -1,
    **kwargs: object,
) -> Array:
    return xp.cross(x1, x2, axis=axis, **kwargs)


def cross(x1: Array, x2: Array, /, *, axis: int = -1) -> Array:
    x1, x2 = _fix_promotion(x1, x2, only_scalar=False)
    if not (-min(x1.ndim, x2.ndim) <= axis < max(x1.ndim, x2.ndim)):
        raise ValueError(f"axis {axis} out of bounds for cross product of arrays with shapes {x1.shape} and {x2.shape}")
    if not (x1.shape[axis] == x2.shape[axis] == 3):
        raise ValueError(f"cross product axis must have size 3, got {x1.shape[axis]} and {x2.shape[axis]}")
    x1, x2 = torch.broadcast_tensors(x1, x2)
    return torch.linalg.cross(x1, x2, dim=axis)


def cross(x1, x2, /, *, axis=-1):
    """
    Returns the cross product of 3-element vectors.

    If ``x1`` and/or ``x2`` are multi-dimensional arrays, then
    the cross-product of each pair of corresponding 3-element vectors
    is independently computed.

    This function is Array API compatible, contrary to
    :func:`numpy.cross`.

    Parameters
    ----------
    x1 : array_like
        The first input array.
    x2 : array_like
        The second input array. Must be compatible with ``x1`` for all
        non-compute axes. The size of the axis over which to compute
        the cross-product must be the same size as the respective axis
        in ``x1``.
    axis : int, optional
        The axis (dimension) of ``x1`` and ``x2`` containing the vectors for
        which to compute the cross-product. Default: ``-1``.

    Returns
    -------
    out : ndarray
        An array containing the cross products.

    See Also
    --------
    numpy.cross

    Examples
    --------
    Vector cross-product.

    >>> x = np.array([1, 2, 3])
    >>> y = np.array([4, 5, 6])
    >>> np.linalg.cross(x, y)
    array([-3,  6, -3])

    Multiple vector cross-products. Note that the direction of the cross
    product vector is defined by the *right-hand rule*.

    >>> x = np.array([[1,2,3], [4,5,6]])
    >>> y = np.array([[4,5,6], [1,2,3]])
    >>> np.linalg.cross(x, y)
    array([[-3,  6, -3],
           [ 3, -6,  3]])

    >>> x = np.array([[1, 2], [3, 4], [5, 6]])
    >>> y = np.array([[4, 5], [6, 1], [2, 3]])
    >>> np.linalg.cross(x, y, axis=0)
    array([[-24,  6],
           [ 18, 24],
           [-6,  -18]])

    """
    x1 = asanyarray(x1)
    x2 = asanyarray(x2)
    return _core_cross(x1, x2, axis=axis)


def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):
    """
    Return the cross product of two (arrays of) vectors.

    The cross product of `a` and `b` in :math:`R^3` is a vector perpendicular
    to both `a` and `b`.  If `a` and `b` are arrays of vectors, the vectors
    are defined by the last axis of `a` and `b` by default, and these axes
    must have 3 dimensions.

    Parameters
    ----------
    a : array_like
        Components of the first vector(s).
    b : array_like
        Components of the second vector(s).
    axisa : int, optional
        Axis of `a` that defines the vector(s).  By default, the last axis.
    axisb : int, optional
        Axis of `b` that defines the vector(s).  By default, the last axis.
    axisc : int, optional
        Axis of `c` containing the cross product vector(s).  By default, the last axis.
    axis : int, optional
        If defined, the axis of `a`, `b` and `c` that defines the vector(s)
        and cross product(s).  Overrides `axisa`, `axisb` and `axisc`.

    Returns
    -------
    c : ndarray
        Vector cross product(s).

    Raises
    ------
    ValueError
        When the dimension of the vector(s) in `a` or `b` does not equal 3.

    See Also
    --------
    inner : Inner product
    outer : Outer product.
    linalg.cross : An Array API compatible variation of ``np.cross``.
    ix_ : Construct index arrays.

    Notes
    -----
    Supports full broadcasting of the inputs.

    Examples
    --------
    Vector cross-product.

    >>> import numpy as np
    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([-3,  6, -3])

    One vector with dimension 2.

    >>> x = [1, 2, 0]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([12, -6, -3])

    Both vectors with dimension 2.

    >>> x = [1, 2, 0]
    >>> y = [4, 5, 0]
    >>> np.cross(x, y)
    array([0, 0, -3])

    Multiple vector cross-products. Note that the direction of the cross
    product vector is defined by the *right-hand rule*.

    >>> x = np.array([[1,2,3], [4,5,6]])
    >>> y = np.array([[4,5,6], [1,2,3]])
    >>> np.cross(x, y)
    array([[-3,  6, -3],
           [ 3, -6,  3]])

    The orientation of `c` can be changed using the `axisc` keyword.

    >>> np.cross(x, y, axisc=0)
    array([[-3,  3],
           [ 6, -6],
           [-3,  3]])

    Change the vector definition of `x` and `y` using `axisa` and `axisb`.

    >>> x = np.array([[1,2,3], [4,5,6], [7, 8, 9]])
    >>> y = np.array([[7, 8, 9], [4,5,6], [1,2,3]])
    >>> np.cross(x, y)
    array([[ -6,  12,  -6],
           [  0,   0,   0],
           [  6, -12,   6]])
    >>> np.cross(x, y, axisa=0, axisb=0)
    array([[-24,  48, -24],
           [-30,  60, -30],
           [-36,  72, -36]])

    """
    if axis is not None:
        axisa, axisb, axisc = (axis,) * 3
    a = asarray(a)
    b = asarray(b)

    if (a.ndim < 1) or (b.ndim < 1):
        raise ValueError("At least one array has zero dimension")

    # Check axisa and axisb are within bounds
    axisa = normalize_axis_index(axisa, a.ndim, msg_prefix='axisa')
    axisb = normalize_axis_index(axisb, b.ndim, msg_prefix='axisb')

    # Move working axis to the end of the shape
    a = moveaxis(a, axisa, -1)
    b = moveaxis(b, axisb, -1)
    if a.shape[-1] != 3 or b.shape[-1] != 3:
        raise ValueError(
            f"Both input arrays must be (arrays of) 3-dimensional vectors, "
            f"but they are {a.shape[-1]} and {b.shape[-1]} dimensional instead."
        )

    # Create the output array
    shape = *broadcast(a[..., 0], b[..., 0]).shape, 3
    # Check axisc is within bounds
    axisc = normalize_axis_index(axisc, len(shape), msg_prefix='axisc')
    dtype = promote_types(a.dtype, b.dtype)
    cp = empty(shape, dtype)

    # recast arrays as dtype
    a = a.astype(dtype)
    b = b.astype(dtype)

    # create local aliases for readability
    a0 = a[..., 0]
    a1 = a[..., 1]
    a2 = a[..., 2]
    b0 = b[..., 0]
    b1 = b[..., 1]
    b2 = b[..., 2]
    cp0 = cp[..., 0]
    cp1 = cp[..., 1]
    cp2 = cp[..., 2]

    # cp0 = a1 * b2 - a2 * b1
    # cp1 = a2 * b0 - a0 * b2
    # cp2 = a0 * b1 - a1 * b0
    multiply(a1, b2, out=cp0)
    tmp = np.multiply(a2, b1, out=...)
    cp0 -= tmp
    multiply(a2, b0, out=cp1)
    multiply(a0, b2, out=tmp)
    cp1 -= tmp
    multiply(a0, b1, out=cp2)
    multiply(a1, b0, out=tmp)
    cp2 -= tmp

    return moveaxis(cp, -1, axisc)


def cross(a, b, axisa: int = -1, axisb: int = -1, axisc: int = -1,
          axis: int | None = None):
  r"""Compute the (batched) cross product of two arrays.

  JAX implementation of :func:`numpy.cross`.

  This computes the 2-dimensional or 3-dimensional cross product,

  .. math::

     c = a \times b

  In 3 dimensions, ``c`` is a length-3 array. In 2 dimensions, ``c`` is
  a scalar.

  Args:
    a: N-dimensional array. ``a.shape[axisa]`` indicates the dimension of
       the cross product, and must be 2 or 3.
    b: N-dimensional array. Must have ``b.shape[axisb] == a.shape[axisb]``,
      and other dimensions of ``a`` and ``b`` must be broadcast compatible.
    axisa: specicy the axis of ``a`` along which to compute the cross product.
    axisb: specicy the axis of ``b`` along which to compute the cross product.
    axisc: specicy the axis of ``c`` along which the cross product result
      will be stored.
    axis: if specified, this overrides ``axisa``, ``axisb``, and ``axisc``
      with a single value.

  Returns:
    The array ``c`` containing the (batched) cross product of ``a`` and ``b``
    along the specified axes.

  See also:
    - :func:`jax.numpy.linalg.cross`: an array API compatible function for
      computing cross products over 3-vectors.

  Examples:
    A 2-dimensional cross product returns a scalar:

    >>> a = jnp.array([1, 2])
    >>> b = jnp.array([3, 4])
    >>> jnp.cross(a, b)
    Array(-2, dtype=int32)

    A 3-dimensional cross product returns a length-3 vector:

    >>> a = jnp.array([1, 2, 3])
    >>> b = jnp.array([4, 5, 6])
    >>> jnp.cross(a, b)
    Array([-3,  6, -3], dtype=int32)

    With multi-dimensional inputs, the cross-product is computed along
    the last axis by default. Here's a batched 3-dimensional cross
    product, operating on the rows of the inputs:

    >>> a = jnp.array([[1, 2, 3],
    ...                [3, 4, 3]])
    >>> b = jnp.array([[2, 3, 2],
    ...                [4, 5, 6]])
    >>> jnp.cross(a, b)
    Array([[-5,  4, -1],
           [ 9, -6, -1]], dtype=int32)

    Specifying axis=0 makes this a batched 2-dimensional cross product,
    operating on the columns of the inputs:

    >>> jnp.cross(a, b, axis=0)
    Array([-2, -2, 12], dtype=int32)

    Equivalently, we can independently specify the axis of the inputs ``a``
    and ``b`` and the output ``c``:

    >>> jnp.cross(a, b, axisa=0, axisb=0, axisc=0)
    Array([-2, -2, 12], dtype=int32)
  """
  # TODO(jakevdp): NumPy 2.0 deprecates 2D inputs. Follow suit here.
  util.check_arraylike("cross", a, b)
  if axis is not None:
    axisa = axis
    axisb = axis
    axisc = axis
  a = moveaxis(a, axisa, -1)
  b = moveaxis(b, axisb, -1)

  if a.shape[-1] not in (2, 3) or b.shape[-1] not in (2, 3):
    raise ValueError("Dimension must be either 2 or 3 for cross product")

  if a.shape[-1] == 2 and b.shape[-1] == 2:
    return a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]

  a0 = a[..., 0]
  a1 = a[..., 1]
  a2 = a[..., 2] if a.shape[-1] == 3 else array_creation.zeros_like(a0)
  b0 = b[..., 0]
  b1 = b[..., 1]
  b2 = b[..., 2] if b.shape[-1] == 3 else array_creation.zeros_like(b0)
  c = array([a1 * b2 - a2 * b1, a2 * b0 - a0 * b2, a0 * b1 - a1 * b0])
  return moveaxis(c, 0, axisc)


def cross(x1: ArrayLike, x2: ArrayLike, /, *, axis=-1):
  r"""Compute the cross-product of two 3D vectors

  JAX implementation of :func:`numpy.linalg.cross`

  Args:
    x1: N-dimensional array, with ``x1.shape[axis] == 3``
    x2: N-dimensional array, with ``x2.shape[axis] == 3``, and other axes
      broadcast-compatible with ``x1``.
    axis: axis along which to take the cross product (default: -1).

  Returns:
    array containing the result of the cross-product

  See Also:
    :func:`jax.numpy.cross`: more flexible cross-product API.

  Examples:

    Showing that :math:`\hat{x} \times \hat{y} = \hat{z}`:

    >>> x = jnp.array([1., 0., 0.])
    >>> y = jnp.array([0., 1., 0.])
    >>> jnp.linalg.cross(x, y)
    Array([0., 0., 1.], dtype=float32)

    Cross product of :math:`\hat{x}` with all three standard unit vectors,
    via broadcasting:

    >>> xyz = jnp.eye(3)
    >>> jnp.linalg.cross(x, xyz, axis=-1)
    Array([[ 0.,  0.,  0.],
           [ 0.,  0.,  1.],
           [ 0., -1.,  0.]], dtype=float32)
  """
  x1, x2 = ensure_arraylike("jnp.linalg.outer", x1, x2)
  if x1.shape[axis] != 3 or x2.shape[axis] != 3:
    raise ValueError(
        "Both input arrays must be (arrays of) 3-dimensional vectors, "
        f"but they have {x1.shape[axis]=} and {x2.shape[axis]=}"
    )
  return jnp.cross(x1, x2, axis=axis)

