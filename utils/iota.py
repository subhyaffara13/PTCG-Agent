
def iota(
    length,
    *,
    start,
    step,
    dtype,
    device,
    requires_grad,
):
    def fn(index):
        return ops.index_expr(step * index[0] + start, dtype=dtype)

    return Pointwise.create(
        device=decode_device(device),
        dtype=dtype,
        inner_fn=fn,
        ranges=[length],
    )


def iota(output: _ods_ir.Type, dimensions: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return IotaOp(output=output, dimensions=dimensions, loc=loc, ip=ip).result


def iota(output: _ods_ir.Type, iota_dimension: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return IotaOp(output=output, iota_dimension=iota_dimension, loc=loc, ip=ip).result


def iota(output: _ods_ir.Type, iota_dimension: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return IotaOp(output=output, iota_dimension=iota_dimension, loc=loc, ip=ip).result


def iota(ctx: LoweringRuleContext, aval_out, *, dimension: int):
  if not core.is_constant_shape(aval_out.shape):
    shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
    (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
    return hlo.dynamic_iota(
        result_type,
        shape,
        i64_attr(dimension),
    )
  else:
    (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
    return hlo.iota(result_type, i64_attr(dimension))


def iota(dtype: DTypeLike, size: int) -> Array:
  """Wraps XLA's `Iota
  <https://www.openxla.org/xla/operation_semantics#iota>`_
  operator.
  """
  return broadcasted_iota(dtype, (size,), 0)

