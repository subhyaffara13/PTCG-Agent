
def _cmp_lowering_rule(primitive, ctx: LoweringRuleContext, x, y):
  x, y = _bcast(
      x,
      y,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  x_aval, y_aval = ctx.avals_in
  if x_aval.dtype != y_aval.dtype:
    raise ValueError(
        f"Mixed dtype operands in cmp: {x_aval.dtype}, {y_aval.dtype}"
    )
  dtype = x_aval.dtype

  if jnp.issubdtype(dtype, jnp.bool_):
    return lower_fun(
        functools.partial(_cmp_boolean_lowering_helper, primitive),
    )(ctx, x, y)

  if jnp.issubdtype(dtype, jnp.integer):
    is_uint = jnp.issubdtype(dtype, jnp.unsignedinteger)
    pred = (
        _cmpui_lowering_types if is_uint else _cmpsi_lowering_types
    )[primitive]
    predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
    return arith.cmpi(predicate, x, y)

  if jnp.issubdtype(dtype, jnp.floating):
    pred = _cmpf_lowering_types[primitive]
    predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
    return arith.cmpf(predicate, x, y)

  raise NotImplementedError(f"Unsupported dtype in cmp: {dtype}")

