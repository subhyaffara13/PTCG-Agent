
def packbits(a, /, axis=None, bitorder="big"):
    """
    packbits(a, /, axis=None, bitorder='big')

    Packs the elements of a binary-valued array into bits in a uint8 array.

    The result is padded to full bytes by inserting zero bits at the end.

    Parameters
    ----------
    a : array_like
        An array of integers or booleans whose elements should be packed to
        bits.
    axis : int, optional
        The dimension over which bit-packing is done.
        ``None`` implies packing the flattened array.
    bitorder : {'big', 'little'}, optional
        The order of the input bits. 'big' will mimic bin(val),
        ``[0, 0, 0, 0, 0, 0, 1, 1] => 3 = 0b00000011``, 'little' will
        reverse the order so ``[1, 1, 0, 0, 0, 0, 0, 0] => 3``.
        Defaults to 'big'.

    Returns
    -------
    packed : ndarray
        Array of type uint8 whose elements represent bits corresponding to the
        logical (0 or nonzero) value of the input elements. The shape of
        `packed` has the same number of dimensions as the input (unless `axis`
        is None, in which case the output is 1-D).

    See Also
    --------
    unpackbits: Unpacks elements of a uint8 array into a binary-valued output
                array.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[[1,0,1],
    ...                [0,1,0]],
    ...               [[1,1,0],
    ...                [0,0,1]]])
    >>> b = np.packbits(a, axis=-1)
    >>> b
    array([[[160],
            [ 64]],
           [[192],
            [ 32]]], dtype=uint8)

    Note that in binary 160 = 1010 0000, 64 = 0100 0000, 192 = 1100 0000,
    and 32 = 0010 0000.

    """
    return (a,)


def packbits(a: ArrayLike, axis: int | None = None, bitorder: str = "big") -> Array:
  """Pack array of bits into a uint8 array.

  JAX implementation of :func:`numpy.packbits`

  Args:
    a: N-dimensional array of bits to pack.
    axis: optional axis along which to pack bits. If not specified, ``a`` will
      be flattened.
    bitorder: ``"big"`` (default) or ``"little"``: specify whether the bit order
      is big-endian or little-endian.

  Returns:
    A uint8 array of packed values.

  See also:
    - :func:`jax.numpy.unpackbits`: inverse of ``packbits``.

  Examples:
    Packing bits in one dimension:

    >>> bits = jnp.array([0, 0, 0, 0, 0, 1, 1, 1])
    >>> jnp.packbits(bits)
    Array([7], dtype=uint8)
    >>> 0b00000111  # equivalent bit-wise representation:
    7

    Optionally specifying little-endian convention:

    >>> jnp.packbits(bits, bitorder="little")
    Array([224], dtype=uint8)
    >>> 0b11100000  # equivalent bit-wise representation
    224

    If the number of bits is not a multiple of 8, it will be right-padded
    with zeros:

    >>> jnp.packbits(jnp.array([1, 0, 1]))
    Array([160], dtype=uint8)
    >>> jnp.packbits(jnp.array([1, 0, 1, 0, 0, 0, 0, 0]))
    Array([160], dtype=uint8)

    For a multi-dimensional input, bits may be packed along a specified axis:

    >>> a = jnp.array([[1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
    ...                [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1]])
    >>> vals = jnp.packbits(a, axis=1)
    >>> vals
    Array([[212, 150],
           [ 69, 207]], dtype=uint8)

    The inverse of ``packbits`` is provided by :func:`~jax.numpy.unpackbits`:

    >>> jnp.unpackbits(vals, axis=1)
    Array([[1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
           [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1]], dtype=uint8)
  """
  arr = util.ensure_arraylike("packbits", a)
  if not (issubdtype(arr.dtype, np.integer) or issubdtype(arr.dtype, np.bool_)):
    raise TypeError('Expected an input array of integer or boolean data type')
  if bitorder not in ['little', 'big']:
    raise ValueError("'order' must be either 'little' or 'big'")
  arr = lax.ne(arr, lax._const(arr, 0)).astype('uint8')
  bits = arange(8, dtype='uint8')
  if bitorder == 'big':
    bits = bits[::-1]
  if axis is None:
    arr = ravel(arr)
    axis = 0
  arr = swapaxes(arr, axis, -1)

  remainder = arr.shape[-1] % 8
  if remainder:
    arr = lax.pad(arr, np.uint8(0),
                  (arr.ndim - 1) * [(0, 0, 0)] + [(0, 8 - remainder, 0)])

  arr = arr.reshape(arr.shape[:-1] + (arr.shape[-1] // 8, 8))
  bits = expand_dims(bits, tuple(range(arr.ndim - 1)))
  packed = (arr << bits).sum(-1).astype('uint8')
  return swapaxes(packed, axis, -1)

