
def fromfunction(function, shape, *, dtype=float, like=None, **kwargs):
    """
    Construct an array by executing a function over each coordinate.

    The resulting array therefore has a value ``fn(x, y, z)`` at
    coordinate ``(x, y, z)``.

    Parameters
    ----------
    function : callable
        The function is called with N parameters, where N is the rank of
        `shape`.  Each parameter represents the coordinates of the array
        varying along a specific axis.  For example, if `shape`
        were ``(2, 2)``, then the parameters would be
        ``array([[0, 0], [1, 1]])`` and ``array([[0, 1], [0, 1]])``
    shape : (N,) tuple of ints
        Shape of the output array, which also determines the shape of
        the coordinate arrays passed to `function`.
    dtype : data-type, optional
        Data-type of the coordinate arrays passed to `function`.
        By default, `dtype` is float.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    fromfunction : any
        The result of the call to `function` is passed back directly.
        Therefore the shape of `fromfunction` is completely determined by
        `function`.  If `function` returns a scalar value, the shape of
        `fromfunction` would not match the `shape` parameter.

    See Also
    --------
    indices, meshgrid

    Notes
    -----
    Keywords other than `dtype` and `like` are passed to `function`.

    Examples
    --------
    >>> import numpy as np
    >>> np.fromfunction(lambda i, j: i, (2, 2), dtype=np.float64)
    array([[0., 0.],
           [1., 1.]])

    >>> np.fromfunction(lambda i, j: j, (2, 2), dtype=np.float64)
    array([[0., 1.],
           [0., 1.]])

    >>> np.fromfunction(lambda i, j: i == j, (3, 3), dtype=np.int_)
    array([[ True, False, False],
           [False,  True, False],
           [False, False,  True]])

    >>> np.fromfunction(lambda i, j: i + j, (3, 3), dtype=np.int_)
    array([[0, 1, 2],
           [1, 2, 3],
           [2, 3, 4]])

    """
    if like is not None:
        return _fromfunction_with_like(
                like, function, shape, dtype=dtype, **kwargs)

    args = indices(shape, dtype=dtype)
    return function(*args, **kwargs)


def fromfunction(function: Callable[..., Array], shape: Any,
                 *, dtype: DTypeLike = float, **kwargs) -> Array:
  """Create an array from a function applied over indices.

  JAX implementation of :func:`numpy.fromfunction`. The JAX implementation
  differs in that it dispatches via :func:`jax.vmap`, and so unlike in NumPy
  the function logically operates on scalar inputs, and need not explicitly
  handle broadcasted inputs (See *Examples* below).

  Args:
    function: a function that takes *N* dynamic scalars and outputs a scalar.
    shape: a length-*N* tuple of integers specifying the output shape.
    dtype: optionally specify the dtype of the inputs. Defaults to floating-point.
    kwargs: additional keyword arguments are passed statically to ``function``.

  Returns:
    An array of shape ``shape`` if ``function`` returns a scalar, or in general
    a pytree of arrays with leading dimensions ``shape``, as determined by the
    output of ``function``.

  See also:
    - :func:`jax.vmap`: the core transformation that the :func:`fromfunction`
      API is built on.

  Examples:
    Generate a multiplication table of a given shape:

    >>> jnp.fromfunction(jnp.multiply, shape=(3, 6), dtype=int)
    Array([[ 0,  0,  0,  0,  0,  0],
           [ 0,  1,  2,  3,  4,  5],
           [ 0,  2,  4,  6,  8, 10]], dtype=int32)

    When ``function`` returns a non-scalar the output will have leading
    dimension of ``shape``:

    >>> def f(x):
    ...   return (x + 1) * jnp.arange(3)
    >>> jnp.fromfunction(f, shape=(2,))
    Array([[0., 1., 2.],
           [0., 2., 4.]], dtype=float32)

    ``function`` may return multiple results, in which case each is mapped
    independently:

    >>> def f(x, y):
    ...   return x + y, x * y
    >>> x_plus_y, x_times_y = jnp.fromfunction(f, shape=(3, 5))
    >>> print(x_plus_y)
    [[0. 1. 2. 3. 4.]
     [1. 2. 3. 4. 5.]
     [2. 3. 4. 5. 6.]]
    >>> print(x_times_y)
    [[0. 0. 0. 0. 0.]
     [0. 1. 2. 3. 4.]
     [0. 2. 4. 6. 8.]]

    The JAX implementation differs slightly from NumPy's implementation. In
    :func:`numpy.fromfunction`, the function is expected to explicitly operate
    element-wise on the full grid of input values:

    >>> def f(x, y):
    ...   print(f"{x.shape = }\\n{y.shape = }")
    ...   return x + y
    ...
    >>> np.fromfunction(f, (2, 3))
    x.shape = (2, 3)
    y.shape = (2, 3)
    array([[0., 1., 2.],
           [1., 2., 3.]])

    In :func:`jax.numpy.fromfunction`, the function is vectorized via
    :func:`jax.vmap`, and so is expected to operate on scalar values:

    >>> jnp.fromfunction(f, (2, 3))
    x.shape = ()
    y.shape = ()
    Array([[0., 1., 2.],
           [1., 2., 3.]], dtype=float32)
  """
  shape = core.canonicalize_shape(shape, context="shape argument of jnp.fromfunction()")
  for i in range(len(shape)):
    in_axes = [0 if i == j else None for j in range(len(shape))]
    function = api.vmap(function, in_axes=tuple(in_axes[::-1]))
  return function(*(arange(s, dtype=dtype) for s in shape), **kwargs)

