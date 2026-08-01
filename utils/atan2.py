
def atan2(a, b):
    return prims.atan2(a, b)


def atan2(g: jit_utils.GraphContext, self, other):
    # self is y, and other is x on coordinate
    slope = g.op("Div", self, other)
    atan = g.op("Atan", slope)
    const_zero = g.op("Constant", value_t=torch.tensor(0))
    const_pi = g.op("Constant", value_t=torch.tensor(math.pi))

    condition_second_or_third_quadrant = g.op("Greater", self, const_zero)
    second_third_quadrant = g.op(
        "Where",
        condition_second_or_third_quadrant,
        g.op("Add", atan, const_pi),
        g.op("Sub", atan, const_pi),
    )

    condition_14_or_23_quadrant = g.op("Less", other, const_zero)
    result = g.op("Where", condition_14_or_23_quadrant, second_third_quadrant, atan)

    return result


def atan2(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return Atan2Op(lhs=lhs, rhs=rhs, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def atan2(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return Atan2Op(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def atan2(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return Atan2Op(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def atan2(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise two-term arc tangent: :math:`\mathrm{atan}({x \over y})`.

  This function lowers directly to the `stablehlo.atan2`_ operation.

  Args:
    x, y: input arrays. Must have a matching floating-point or complex dtypes. If
      neither is a scalar, the two arrays must have the same number of dimensions
      and be broadcast-compatible.

  Returns:
    Array of the same shape and dtype as ``x`` and ``y`` containing the element-wise
    arc tangent of :math:`x \over y`, respecting the quadrant indicated by the sign
    of each input.

  See also:
    - :func:`jax.lax.tan`: elementwise tangent.
    - :func:`jax.lax.atan`: elementwise one-term arc tangent.

  .. _stablehlo.atan2: https://openxla.org/stablehlo/spec#atan2
  """
  x, y = core.auto_insert_reshard(x, y)
  return atan2_p.bind(x, y)


def atan2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arctan2`"""
  return arctan2(*promote_args('atan2', x1, x2))

