
def left_shift(a, n):
    """
    Shift the bits of an integer to the left.

    This is the masked array version of `numpy.left_shift`, for details
    see that function.

    See Also
    --------
    numpy.left_shift

    Examples
    --------
    Shift with a masked array:

    >>> arr = np.ma.array([10, 20, 30], mask=[False, True, False])
    >>> np.ma.left_shift(arr, 1)
    masked_array(data=[20, --, 60],
                 mask=[False,  True, False],
           fill_value=999999)

    Large shift:

    >>> np.ma.left_shift(10, 10)
    masked_array(data=10240,
                 mask=False,
           fill_value=999999)

    Shift with a scalar and an array:

    >>> scalar = 10
    >>> arr = np.ma.array([1, 2, 3], mask=[False, True, False])
    >>> np.ma.left_shift(scalar, arr)
    masked_array(data=[20, --, 80],
                 mask=[False,  True, False],
           fill_value=999999)


    """
    m = getmask(a)
    if m is nomask:
        d = umath.left_shift(filled(a), n)
        return masked_array(d)
    else:
        d = umath.left_shift(filled(a, 0), n)
        return masked_array(d, mask=m)


def left_shift(x: ArrayLike, y: ArrayLike, /) -> Array:
  r"""Shift bits of ``x`` to left by the amount specified in ``y``, element-wise.

  JAX implementation of :obj:`numpy.left_shift`.

  Args:
    x: Input array, must be integer-typed.
    y: The amount of bits to shift each element in ``x`` to the left, only accepts
      integer subtypes. ``x`` and ``y`` must either have same shape or be broadcast
      compatible.

  Returns:
    An array containing the left shifted elements of ``x`` by the amount specified
    in ``y``, with the same shape as the broadcasted shape of ``x`` and ``y``.

  Note:
    Left shifting ``x`` by ``y`` is equivalent to ``x * (2**y)`` within the
    bounds of the dtypes involved.

  See also:
    - :func:`jax.numpy.right_shift`: and :func:`jax.numpy.bitwise_right_shift`:
      Shifts the bits of ``x1`` to right by the amount specified in ``x2``,
      element-wise.
    - :func:`jax.numpy.bitwise_left_shift`: Alias of :func:`jax.left_shift`.

  Examples:
    >>> def print_binary(x):
    ...   return [bin(int(val)) for val in x]

    >>> x1 = jnp.arange(5)
    >>> x1
    Array([0, 1, 2, 3, 4], dtype=int32)
    >>> print_binary(x1)
    ['0b0', '0b1', '0b10', '0b11', '0b100']
    >>> x2 = 1
    >>> result = jnp.left_shift(x1, x2)
    >>> result
    Array([0, 2, 4, 6, 8], dtype=int32)
    >>> print_binary(result)
    ['0b0', '0b10', '0b100', '0b110', '0b1000']

    >>> x3 = 4
    >>> print_binary([x3])
    ['0b100']
    >>> x4 = jnp.array([1, 2, 3, 4])
    >>> result1 = jnp.left_shift(x3, x4)
    >>> result1
    Array([ 8, 16, 32, 64], dtype=int32)
    >>> print_binary(result1)
    ['0b1000', '0b10000', '0b100000', '0b1000000']
  """
  return lax.shift_left(*promote_args_numeric("left_shift", x, y))

