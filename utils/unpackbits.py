
def unpackbits(a, /, axis=None, count=None, bitorder="big"):
    """
    unpackbits(a, /, axis=None, count=None, bitorder='big')

    Unpacks elements of a uint8 array into a binary-valued output array.

    Each element of `a` represents a bit-field that should be unpacked
    into a binary-valued output array. The shape of the output array is
    either 1-D (if `axis` is ``None``) or the same shape as the input
    array with unpacking done along the axis specified.

    Parameters
    ----------
    a : ndarray, uint8 type
       Input array.
    axis : int, optional
        The dimension over which bit-unpacking is done.
        ``None`` implies unpacking the flattened array.
    count : int or None, optional
        The number of elements to unpack along `axis`, provided as a way
        of undoing the effect of packing a size that is not a multiple
        of eight. A non-negative number means to only unpack `count`
        bits. A negative number means to trim off that many bits from
        the end. ``None`` means to unpack the entire array (the
        default). Counts larger than the available number of bits will
        add zero padding to the output. Negative counts must not
        exceed the available number of bits.
    bitorder : {'big', 'little'}, optional
        The order of the returned bits. 'big' will mimic bin(val),
        ``3 = 0b00000011 => [0, 0, 0, 0, 0, 0, 1, 1]``, 'little' will reverse
        the order to ``[1, 1, 0, 0, 0, 0, 0, 0]``.
        Defaults to 'big'.

    Returns
    -------
    unpacked : ndarray, uint8 type
       The elements are binary-valued (0 or 1).

    See Also
    --------
    packbits : Packs the elements of a binary-valued array into bits in
               a uint8 array.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[2], [7], [23]], dtype=np.uint8)
    >>> a
    array([[ 2],
           [ 7],
           [23]], dtype=uint8)
    >>> b = np.unpackbits(a, axis=1)
    >>> b
    array([[0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 0, 1, 1, 1]], dtype=uint8)
    >>> c = np.unpackbits(a, axis=1, count=-3)
    >>> c
    array([[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0]], dtype=uint8)

    >>> p = np.packbits(b, axis=0)
    >>> np.unpackbits(p, axis=0)
    array([[0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 0, 1, 1, 1],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    >>> np.array_equal(b, np.unpackbits(p, axis=0, count=b.shape[0]))
    True

    """
    return (a,)


def unpackbits(
    a: ArrayLike,
    axis: int | None = None,
    count: int | None = None,
    bitorder: str = "big",
) -> Array:
  """Unpack the bits in a uint8 array.

  JAX implementation of :func:`numpy.unpackbits`.

  Args:
    a: N-dimensional array of type ``uint8``.
    axis: optional axis along which to unpack. If not specified, ``a`` will
      be flattened
    count: specify the number of bits to unpack (if positive) or the number
      of bits to trim from the end (if negative).
    bitorder: ``"big"`` (default) or ``"little"``: specify whether the bit order
      is big-endian or little-endian.

  Returns:
    a uint8 array of unpacked bits.

  See also:
    - :func:`jax.numpy.packbits`: this inverse of ``unpackbits``.

  Examples:
    Unpacking bits from a scalar:

    >>> jnp.unpackbits(jnp.uint8(27))  # big-endian by default
    Array([0, 0, 0, 1, 1, 0, 1, 1], dtype=uint8)
    >>> jnp.unpackbits(jnp.uint8(27), bitorder="little")
    Array([1, 1, 0, 1, 1, 0, 0, 0], dtype=uint8)

    Compare this to the Python binary representation:

    >>> 0b00011011
    27

    Unpacking bits along an axis:

    >>> vals = jnp.array([[154],
    ...                   [ 49]], dtype='uint8')
    >>> bits = jnp.unpackbits(vals, axis=1)
    >>> bits
    Array([[1, 0, 0, 1, 1, 0, 1, 0],
           [0, 0, 1, 1, 0, 0, 0, 1]], dtype=uint8)

    Using :func:`~jax.numpy.packbits` to invert this:

    >>> jnp.packbits(bits, axis=1)
    Array([[154],
           [ 49]], dtype=uint8)

    The ``count`` keyword lets ``unpackbits`` serve as an inverse of ``packbits``
    in cases where not all bits are present:

    >>> bits = jnp.array([1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1])  # 11 bits
    >>> vals = jnp.packbits(bits)
    >>> vals
    Array([219,  96], dtype=uint8)
    >>> jnp.unpackbits(vals)  # 16 zero-padded bits
    Array([1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0], dtype=uint8)
    >>> jnp.unpackbits(vals, count=11)  # specify 11 output bits
    Array([1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1], dtype=uint8)
    >>> jnp.unpackbits(vals, count=-5)  # specify 5 bits to be trimmed
    Array([1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1], dtype=uint8)
  """
  arr = util.ensure_arraylike("unpackbits", a)
  if arr.dtype != np.uint8:
    raise TypeError("Expected an input array of unsigned byte data type")
  if bitorder not in ['little', 'big']:
    raise ValueError("'order' must be either 'little' or 'big'")
  bits = asarray(1) << arange(8, dtype='uint8')
  if bitorder == 'big':
    bits = bits[::-1]
  if axis is None:
    arr = ravel(arr)
    axis = 0
  arr = swapaxes(arr, axis, -1)
  unpacked = ((arr[..., None] & expand_dims(bits, tuple(range(arr.ndim)))) > 0).astype('uint8')
  unpacked = unpacked.reshape(unpacked.shape[:-2] + (-1,))
  if count is not None:
    if count > unpacked.shape[-1]:
      unpacked = pad(unpacked, [(0, 0)] * (unpacked.ndim - 1) + [(0, count - unpacked.shape[-1])])
    else:
      unpacked = unpacked[..., :count]
  return swapaxes(unpacked, axis, -1)

