
def subtract(
    image1: Image.Image, image2: Image.Image, scale: float = 1.0, offset: float = 0
) -> Image.Image:
    """
    Subtracts two images, dividing the result by scale and adding the offset.
    If omitted, scale defaults to 1.0, and offset to 0.0. ::

        out = ((image1 - image2) / scale + offset)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_subtract(image2.im, scale, offset))


def subtract(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SubtractOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def subtract(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SubtractOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def subtract(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Subtract two arrays element-wise.

  JAX implementation of :obj:`numpy.subtract`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.
  This function provides the implementation of the ``-`` operator for
  JAX arrays.

  Args:
    x, y: arrays to subtract. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise subtraction.

  Examples:
    Calling ``subtract`` explicitly:

    >>> x = jnp.arange(4)
    >>> jnp.subtract(x, 10)
    Array([-10,  -9,  -8,  -7], dtype=int32)

    Calling ``subtract`` via the ``-`` operator:

    >>> x - 10
    Array([-10,  -9,  -8,  -7], dtype=int32)
  """
  out = lax.sub(*promote_args("subtract", x, y))
  jnp_error._set_error_if_nan(out)
  return out

