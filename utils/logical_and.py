
def logical_and(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """Logical AND between two images.

    Both of the images must have mode "1". If you would like to perform a
    logical AND on an image with a mode other than "1", try
    :py:meth:`~PIL.ImageChops.multiply` instead, using a black-and-white mask
    as the second image. ::

        out = ((image1 and image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_and(image2.im))


def logical_and(a: TensorLikeType, b: TensorLikeType):
    if not utils.is_boolean_dtype(a.dtype):
        a = a != 0
    if not utils.is_boolean_dtype(b.dtype):
        b = b != 0
    return a & b


def logical_and(g: jit_utils.GraphContext, input, other):
    return g.op("And", input, other)


def logical_and(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the logical AND operation elementwise.

  JAX implementation of :obj:`numpy.logical_and`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: input arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise logical AND.

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.logical_and(x, 1)
    Array([False,  True,  True,  True], dtype=bool)
  """
  return lax.bitwise_and(*map(_to_bool, promote_args("logical_and", x, y)))

