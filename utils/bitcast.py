import math


def bitcast(result: _ods_ir.Type, src: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BitcastOp(result=result, src=src, loc=loc, ip=ip).result


def bitcast(output: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return BitcastOp(output=output, input=input, loc=loc, ip=ip).result


def bitcast(out: _ods_ir.Type, in_: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BitcastOp(out=out, in_=in_, loc=loc, ip=ip).result


def bitcast(res: _ods_ir.Type, arg: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BitcastOp(res=res, arg=arg, loc=loc, ip=ip).result


def bitcast(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BitcastOp(result=result, operand=operand, loc=loc, ip=ip).result


def bitcast(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return BitCastOp(result=result, source=source, loc=loc, ip=ip).result


def bitcast(x, dtype: DTypeLike):
  x_bitwidth = dtypes.itemsize_bits(x.dtype)
  y_bitwidth = dtypes.itemsize_bits(dtype)
  shape = list(x.shape)
  if x_bitwidth != y_bitwidth:
    if len(shape) < 2:
      raise NotImplementedError(
          "Bitcast 1D ref with bitwidth change is not supported."
      )
    # Note: this is only valid on TPU.
    if shape[-2] * x_bitwidth % y_bitwidth != 0:
      raise ValueError(
          "Expected input and output shapes are the same after multiplying"
          " the second-minor dimension by the bitwidths."
      )
  shape[-2] = shape[-2] * x_bitwidth // y_bitwidth
  if x_bitwidth < y_bitwidth:
    ratio = y_bitwidth // x_bitwidth
    x = x.reshape(*x.shape[:-2], x.shape[-2] // ratio, ratio, -1).swapaxes(
        -1, -2
    )
  y = lax.bitcast_convert_type(x, dtype)
  if x_bitwidth > y_bitwidth:
    y = y.swapaxes(-1, -2).reshape(shape)
  return y


def bitcast(x: jax.Array, ty: DTypeLike) -> jax.Array:
  ty = dtypes.check_and_canonicalize_user_dtype(ty)
  if len(x.shape) < 2:
    raise ValueError("Not implemented: bitcast 1D")
  src_bitwidth = dtypes.itemsize_bits(x.dtype)
  dst_bitwidth = dtypes.itemsize_bits(ty)
  if x.shape[-2] * src_bitwidth % dst_bitwidth:
    raise ValueError(
        "Not implemented: the 2nd minor dim can not be perfectly packed or"
        " unpacked"
    )
  return bitcast_p.bind(x, ty=ty)


def bitcast(x: jax.Array, dtype: jax.typing.DTypeLike) -> jax.Array:
  """Bitcasts an array to a different dtype.

  Unlike ``lax.bitcast_convert_type``, this function returns an array of the
  same rank as the input. The minormost dimension is expanded/shrunk to
  account for the difference in the element bitwidth.
  """
  if x.dtype == dtype:
    return x
  return bitcast_p.bind(x, dtype=jnp.dtype(dtype))


def bitcast(x: ir.Value, new_type: ir.Type):
  if x.type == new_type:
    return x
  if (x_bw := bitwidth(x.type)) != (new_bw := bitwidth(new_type)):
    raise ValueError(
        f"Can't bitcast {x.type} (of bitwidth {x_bw}) to {new_type} (of"
        f" bitwidth {new_bw})"
    )
  if isinstance(x.type, ir.VectorType) and isinstance(new_type, ir.IntegerType):
    new_type = ir.IntegerType(new_type)
    x_ty = ir.VectorType(x.type)
    assert new_type.width == bitwidth(x_ty.element_type) * math.prod(x_ty.shape)
    return vector.extract(
        vector.bitcast(ir.VectorType.get((1,), new_type), x),
        dynamic_position=[],
        static_position=ir.DenseI64ArrayAttr.get([0]),
    )
  if isinstance(x.type, ir.IntegerType) and isinstance(new_type, ir.VectorType):
    new_type = ir.VectorType(new_type)
    x_ty = ir.IntegerType(x.type)
    assert x_ty.width == bitwidth(new_type.element_type) * math.prod(
        new_type.shape
    )
    return vector.bitcast(
        new_type, vector.broadcast(ir.VectorType.get((1,), x_ty), x)
    )
  if isinstance(x.type, ir.VectorType) and isinstance(new_type, ir.VectorType):
    x_ty = ir.VectorType(x.type)
    new_ty = ir.VectorType(new_type)
    if bitwidth(x_ty) != bitwidth(new_ty):
      raise ValueError(f"Can't bitcast {x.type} to {new_type}")
    return vector.bitcast(new_type, x)
  if isinstance(x.type, ir.IntegerType) and isinstance(new_type, ir.FloatType):
    return arith.bitcast(new_type, x)
  if isinstance(x.type, ir.FloatType) and isinstance(new_type, ir.IntegerType):
    return arith.bitcast(new_type, x)
  if isinstance(x.type, ir.FloatType) and isinstance(new_type, ir.FloatType):
    return arith.bitcast(new_type, x)
  raise ValueError(f"Can't bitcast {x.type} to {new_type}")

