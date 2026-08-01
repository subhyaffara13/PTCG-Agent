
def _convert_element_type_lowering_rule_wg(
    ctx: LoweringRuleContext, x, *, new_dtype, weak_type, sharding
):
  del weak_type, sharding
  [x_aval] = ctx.avals_in
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if x_aval.shape:
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
  [y_aval] = ctx.avals_out
  x = _ensure_ir_value(x, x_aval.dtype)

  cur_dtype = mgpu_utils.dtype_to_ir_type(x_aval.dtype)
  new_dtype = mgpu_utils.dtype_to_ir_type(new_dtype)

  if cur_dtype == new_dtype:
    return x

  from_float = isinstance(cur_dtype, ir.FloatType)
  to_float = isinstance(new_dtype, ir.FloatType)
  from_integer = isinstance(cur_dtype, ir.IntegerType)
  to_integer = isinstance(new_dtype, ir.IntegerType)
  if from_float and to_float:
    cur_ty_width = ir.FloatType(cur_dtype).width
    new_ty_width = ir.FloatType(new_dtype).width
    if cur_ty_width == new_ty_width:
      # There is no instruction to perform conversions between two float types
      # of the same width. Go through the next-larger standard type.
      # TODO(bchetioui): support conversions between float types of width 8.
      # Which larger type to pick will depend on the number of bits in the
      # smallest exponent.
      if cur_ty_width != 16:
        raise NotImplementedError(
            "Conversion between float types of width other than 16 not"
            " supported"
        )
      larger_ty = ir.F32Type.get()
      if x_aval.shape:
        upcast_ty = ir.VectorType.get(x_aval.shape, larger_ty)
      else:
        upcast_ty = larger_ty

      def convert(ty, x):
        return arith_dialect.truncf(ty, arith_dialect.extf(upcast_ty, x))

    elif ir.FloatType(cur_dtype).width > ir.FloatType(new_dtype).width:
      convert = arith_dialect.truncf
    else:
      convert = arith_dialect.extf
  elif from_integer and to_integer:
    if ir.IntegerType(cur_dtype).width > ir.IntegerType(new_dtype).width:
      convert = arith_dialect.trunci
    elif ir.IntegerType(cur_dtype).width < ir.IntegerType(new_dtype).width:
      if mgpu_utils.is_signed(x_aval.dtype):
        convert = arith_dialect.extsi
      else:
        convert = arith_dialect.extui
    else:
      convert = lambda _, x: x  # signed <-> unsigned conversions
  elif from_integer and to_float:
    if mgpu_utils.is_signed(x_aval.dtype):
      convert = arith_dialect.sitofp
    else:
      convert = arith_dialect.uitofp
  elif from_float and to_integer:
    dst_width = mgpu_utils.bitwidth(new_dtype)
    # We clamp the float value to the min/max integer destination value
    # in order to match JAX/XLA casting behavior. Note that this differs
    # from numpy casting behavior.
    if mgpu_utils.is_signed(y_aval.dtype):
      maxint = 2 ** (dst_width - 1) - 1
      minint = -(2 ** (dst_width - 1))
      convert = arith_dialect.fptosi
    else:
      maxint = 2**dst_width - 1
      minint = 0
      convert = arith_dialect.fptoui

    maxint = _ir_constant(maxint, cur_dtype)
    minint = _ir_constant(minint, cur_dtype)
    if x_aval.shape:
      maxint = vector_dialect.broadcast(x.type, maxint)
      minint = vector_dialect.broadcast(x.type, minint)
    x = arith_dialect.minimumf(x, maxint)
    x = arith_dialect.maximumf(x, minint)
  else:
    raise NotImplementedError(f"Unsupported conversion {cur_dtype} -> {new_dtype}")

  ty = ir.VectorType.get(x_aval.shape, new_dtype) if x_aval.shape else new_dtype
  return convert(ty, x)

