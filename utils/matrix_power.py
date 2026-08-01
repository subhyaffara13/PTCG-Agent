
def matrix_power(a: ArrayLike, n):
    a = _atleast_float_1(a)
    return torch.linalg.matrix_power(a, n)


def matrix_power(A, power):
    """
    Raise a square matrix to the integer power, `power`.

    For non-negative integers, ``A**power`` is computed using repeated
    matrix multiplications. Negative integers are not supported. 

    Parameters
    ----------
    A : (M, M) square sparse array or matrix
        sparse array that will be raised to power `power`
    power : int
        Exponent used to raise sparse array `A`

    Returns
    -------
    A**power : (M, M) sparse array or matrix
        The output matrix will be the same shape as A, and will preserve
        the class of A, but the format of the output may be changed.
    
    Notes
    -----
    This uses a recursive implementation of the matrix power. For computing
    the matrix power using a reasonably large `power`, this may be less efficient
    than computing the product directly, using A @ A @ ... @ A.
    This is contingent upon the number of nonzero entries in the matrix. 

    .. versionadded:: 1.12.0

    Examples
    --------
    >>> from scipy import sparse
    >>> A = sparse.csc_array([[0,1,0],[1,0,1],[0,1,0]])
    >>> A.todense()
    array([[0, 1, 0],
           [1, 0, 1],
           [0, 1, 0]])
    >>> (A @ A).todense()
    array([[1, 0, 1],
           [0, 2, 0],
           [1, 0, 1]])
    >>> A2 = sparse.linalg.matrix_power(A, 2)
    >>> A2.todense()
    array([[1, 0, 1],
           [0, 2, 0],
           [1, 0, 1]])
    >>> A4 = sparse.linalg.matrix_power(A, 4)
    >>> A4.todense()
    array([[2, 0, 2],
           [0, 4, 0],
           [2, 0, 2]])

    """
    M, N = A.shape
    if M != N:
        raise TypeError('sparse matrix is not square')

    if isintlike(power):
        power = int(power)
        if power < 0:
            raise ValueError('exponent must be >= 0')

        if power == 0:
            return eye_array(M, dtype=A.dtype)

        if power == 1:
            return A.copy()

        tmp = matrix_power(A, power // 2)
        if power % 2:
            return A @ tmp @ tmp
        else:
            return tmp @ tmp
    else:
        raise ValueError("exponent must be an integer")


def matrix_power(a, n):
    """
    Raise a square matrix to the (integer) power `n`.

    For positive integers `n`, the power is computed by repeated matrix
    squarings and matrix multiplications. If ``n == 0``, the identity matrix
    of the same shape as M is returned. If ``n < 0``, the inverse
    is computed and then raised to the ``abs(n)``.

    .. note:: Stacks of object matrices are not currently supported.

    Parameters
    ----------
    a : (..., M, M) array_like
        Matrix to be "powered".
    n : int
        The exponent can be any integer or long integer, positive,
        negative, or zero.

    Returns
    -------
    a**n : (..., M, M) ndarray or matrix object
        The return value is the same shape and type as `M`;
        if the exponent is positive or zero then the type of the
        elements is the same as those of `M`. If the exponent is
        negative the elements are floating-point.

    Raises
    ------
    LinAlgError
        For matrices that are not square or that (for negative powers) cannot
        be inverted numerically.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.linalg import matrix_power
    >>> i = np.array([[0, 1], [-1, 0]]) # matrix equiv. of the imaginary unit
    >>> matrix_power(i, 3) # should = -i
    array([[ 0, -1],
           [ 1,  0]])
    >>> matrix_power(i, 0)
    array([[1, 0],
           [0, 1]])
    >>> matrix_power(i, -3) # should = 1/(-i) = i, but w/ f.p. elements
    array([[ 0.,  1.],
           [-1.,  0.]])

    Somewhat more sophisticated example

    >>> q = np.zeros((4, 4))
    >>> q[0:2, 0:2] = -i
    >>> q[2:4, 2:4] = i
    >>> q # one of the three quaternion units not equal to 1
    array([[ 0., -1.,  0.,  0.],
           [ 1.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.],
           [ 0.,  0., -1.,  0.]])
    >>> matrix_power(q, 2) # = -np.eye(4)
    array([[-1.,  0.,  0.,  0.],
           [ 0., -1.,  0.,  0.],
           [ 0.,  0., -1.,  0.],
           [ 0.,  0.,  0., -1.]])

    """
    a = asanyarray(a)
    _assert_stacked_square(a)

    try:
        n = operator.index(n)
    except TypeError as e:
        raise TypeError("exponent must be an integer") from e

    # Fall back on dot for object arrays. Object arrays are not supported by
    # the current implementation of matmul using einsum
    if a.dtype != object:
        fmatmul = matmul
    elif a.ndim == 2:
        fmatmul = dot
    else:
        raise NotImplementedError(
            "matrix_power not supported for stacks of object arrays")

    if n == 0:
        a = empty_like(a)
        a[...] = eye(a.shape[-2], dtype=a.dtype)
        return a

    elif n < 0:
        a = inv(a)
        n = abs(n)

    # short-cuts.
    if n == 1:
        return a

    elif n == 2:
        return fmatmul(a, a)

    elif n == 3:
        return fmatmul(fmatmul(a, a), a)

    # Use binary decomposition to reduce the number of matrix multiplications.
    # Here, we iterate over the bits of n, from LSB to MSB, raise `a` to
    # increasing powers of 2, and multiply into the result as needed.
    z = result = None
    while n > 0:
        z = a if z is None else fmatmul(z, z)
        n, bit = divmod(n, 2)
        if bit:
            result = z if result is None else fmatmul(result, z)

    return result


def matrix_power(a: ArrayLike, n: int) -> Array:
  """Raise a square matrix to an integer power.

  JAX implementation of :func:`numpy.linalg.matrix_power`, implemented via
  repeated squarings.

  Args:
    a: array of shape ``(..., M, M)`` to be raised to the power `n`.
    n: the integer exponent to which the matrix should be raised.

  Returns:
    Array of shape ``(..., M, M)`` containing the matrix power of a to the n.

  Examples:
    >>> a = jnp.array([[1., 2.],
    ...                [3., 4.]])
    >>> jnp.linalg.matrix_power(a, 3)
    Array([[ 37.,  54.],
           [ 81., 118.]], dtype=float32)
    >>> a @ a @ a  # equivalent evaluated directly
    Array([[ 37.,  54.],
           [ 81., 118.]], dtype=float32)

    This also supports zero powers:

    >>> jnp.linalg.matrix_power(a, 0)
    Array([[1., 0.],
           [0., 1.]], dtype=float32)

    and also supports negative powers:

    >>> with jnp.printoptions(precision=3):
    ...   jnp.linalg.matrix_power(a, -2)
    Array([[ 5.5 , -2.5 ],
           [-3.75,  1.75]], dtype=float32)

    Negative powers are equivalent to matmul of the inverse:

    >>> inv_a = jnp.linalg.inv(a)
    >>> with jnp.printoptions(precision=3):
    ...   inv_a @ inv_a
    Array([[ 5.5 , -2.5 ],
           [-3.75,  1.75]], dtype=float32)
  """
  arr = ensure_arraylike("jnp.linalg.matrix_power", a)

  if arr.ndim < 2:
    raise TypeError("{}-dimensional array given. Array must be at least "
                    "two-dimensional".format(arr.ndim))
  if arr.shape[-2] != arr.shape[-1]:
    raise TypeError("Last 2 dimensions of the array must be square")
  try:
    n = operator.index(n)
  except TypeError as err:
    raise TypeError(f"exponent must be an integer, got {n}") from err

  if n == 0:
    return jnp.broadcast_to(jnp.eye(arr.shape[-2], dtype=arr.dtype), arr.shape)
  elif n < 0:
    arr = inv(arr)
    n = abs(n)

  if n == 1:
    return arr
  elif n == 2:
    return arr @ arr
  elif n == 3:
    return (arr @ arr) @ arr

  z: Array | None = None
  result: Array | None = None
  while n > 0:
    z = arr if z is None else (z @ z)
    n, bit = divmod(n, 2)
    if bit:
      result = z if result is None else (result @ z)
  assert result is not None
  return result

