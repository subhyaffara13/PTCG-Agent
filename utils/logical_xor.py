
def logical_xor(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """Logical XOR between two images.

    Both of the images must have mode "1". ::

        out = ((bool(image1) != bool(image2)) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_xor(image2.im))


def logical_xor(a: TensorLikeType, b: TensorLikeType):
    if not utils.is_boolean_dtype(a.dtype):
        a = a != 0
    if not utils.is_boolean_dtype(b.dtype):
        b = b != 0
    return a ^ b


def logical_xor(g: jit_utils.GraphContext, input, other):
    return g.op("Xor", input, other)


def logical_xor(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the logical XOR operation elementwise.

  JAX implementation of :obj:`numpy.logical_xor`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: input arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise logical XOR.

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.logical_xor(x, 1)
    Array([ True, False, False, False], dtype=bool)
  """
  return lax.bitwise_xor(*map(_to_bool, promote_args("logical_xor", x, y)))

