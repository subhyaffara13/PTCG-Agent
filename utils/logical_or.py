
def logical_or(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """Logical OR between two images.

    Both of the images must have mode "1". ::

        out = ((image1 or image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_or(image2.im))


def logical_or(a: TensorLikeType, b: TensorLikeType):
    if not utils.is_boolean_dtype(a.dtype):
        a = a != 0
    if not utils.is_boolean_dtype(b.dtype):
        b = b != 0
    return bitwise_or(a, b)


def logical_or(g: jit_utils.GraphContext, input, other):
    return g.op("Or", input, other)


def logical_or(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the logical OR operation elementwise.

  JAX implementation of :obj:`numpy.logical_or`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: input arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise logical OR.

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.logical_or(x, 1)
    Array([ True,  True,  True,  True], dtype=bool)
  """
  return lax.bitwise_or(*map(_to_bool, promote_args("logical_or", x, y)))

