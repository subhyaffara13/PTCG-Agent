
def _maybe_cast_load_to_bool(
    ctx: LoweringRuleContext, out_aval, val: ir.Value
) -> ir.Value:
  """Casts a memref load value to bool if the requested value is a bool.

  Mosaic does not support boolean-type memrefs, since booleans
  typically live in mask registers. We instead load booleans as integers from
  memrefs and move them to mask registers on load using this function.

  Args:
    out_aval: The output aval of the load.
    val: The input value.

  Returns:
    The casted value.
  """
  if out_aval.dtype != jnp.bool_:
    return val
  load_scalar_type = _dtype_to_ir_type(BOOL_MEMREF_TYPE)
  pred = _cmpsi_lowering_types[lax.ne_p]
  predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
  const_zero = ir.IntegerAttr.get(load_scalar_type, 0)
  if out_aval.shape:  # Vector case.
    load_vector_type = ctx.aval_to_ir_type(out_aval, is_kernel_boundary=True)
    vector_zeros = arith.constant(
        load_vector_type,
        ir.DenseElementsAttr.get_splat(load_vector_type, const_zero)
    )
    return arith.cmpi(predicate, val, vector_zeros)
  else:  # Scalar case.
    const_zero = arith.constant(load_scalar_type, const_zero)
    return arith.cmpi(predicate, val, const_zero)

