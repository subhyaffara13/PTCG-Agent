
def _scan_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    jaxpr: jax_core.ClosedJaxpr,
    length: int,
    reverse: bool,
    unroll: int,
    num_consts: int,
    num_carry: int,
):
  # Can only handle fori_loop-like scans
  if reverse: raise NotImplementedError
  del reverse

  jaxpr_body, jaxpr_consts = jaxpr.jaxpr, jaxpr.consts
  if jaxpr_consts: raise NotImplementedError
  del jaxpr_consts

  jaxpr_body, has_loop_index = pallas_utils.pattern_match_scan_to_fori_loop(
      jaxpr_body, num_consts, num_carry
  )
  consts, args = split_list(args, [num_consts])
  consts_avals, args_avals = split_list(ctx.avals_in, [num_consts])
  if has_loop_index:
    loop_index_start, *args = args
    loop_index_start = loop_index_start
    args_avals = args_avals[1:]
  else:
    loop_index_start = 0
  consts = map(_ensure_mlir_value, consts, consts_avals)
  args = map(_ensure_mlir_value, args, args_avals)
  out = _lower_jaxpr_to_for_loop(
      ctx, jaxpr_body, loop_index_start, length,
      consts, *args, has_loop_index=has_loop_index,
      unroll=unroll)
  if has_loop_index:
    out = [ir_constant(length, mlir_type=_dtype_to_ir_type(jnp.int32)), *out]
  return out


def _scan_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    jaxpr: jax_core.ClosedJaxpr,
    length: int,
    reverse: bool,
    unroll: int,
    num_consts: int,
    num_carry: int,
):
  # Can only handle fori_loop-like scans.
  if reverse:
    raise NotImplementedError
  del reverse

  jaxpr, jaxpr_consts = jaxpr.jaxpr, jaxpr.consts
  if jaxpr_consts:
    raise NotImplementedError
  del jaxpr_consts

  body_jaxpr, has_loop_index = pallas_utils.pattern_match_scan_to_fori_loop(
      jaxpr, num_consts, num_carry
  )
  consts, args = util.split_list(args, [num_consts])
  _consts_avals, arg_avals = util.split_list(ctx.avals_in, [num_consts])
  if has_loop_index:
    start, *args = args
    index_aval, *_ = arg_avals
    start: ir.Value = _ensure_ir_value(start, index_aval.dtype)
  else:
    start = _i32_constant(0)

  for_out = _lower_jaxpr_to_for_loop(
      ctx,
      body_jaxpr,
      start,
      length,
      consts,
      *args,
      has_loop_index=has_loop_index,
      unroll=unroll,
  )
  if has_loop_index:
    # Need to return the final loop index value if the outer scan expects
    # it as an output.
    loop_index = arith_dialect.addi(start, _ir_constant(length, start.type))
    return [loop_index, *for_out]
  return for_out


def _scan_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    jaxpr,
    length,
    reverse,
    unroll,
    num_consts,
    num_carry,
):
  # Only implements fori_loop-like scans
  if reverse: raise NotImplementedError
  if unroll != 1: raise NotImplementedError
  del unroll, reverse

  jaxpr, jaxpr_consts = jaxpr.jaxpr, jaxpr.consts
  if jaxpr_consts: raise NotImplementedError
  del jaxpr_consts

  jaxpr, has_loop_index = (
      pallas_utils.pattern_match_scan_to_fori_loop(jaxpr, num_consts, num_carry)
  )
  args = map(_ensure_ir_value, args, ctx.avals_in)
  consts, args = util.split_list(args, [num_consts])
  if has_loop_index:
    lower_bound, *args = args
    upper_bound = _add(lower_bound, _ir_constant(length, lower_bound.type))
    bound_type = lower_bound.type
    assert isinstance(bound_type, ir.IntegerType)
  else:
    lower_bound = _i32_constant(0)
    upper_bound = _i32_constant(length)
    bound_type = ir.IntegerType.get_signless(32)
  for_out = _lower_jaxpr_to_for_loop(
      ctx, jaxpr, lower_bound, upper_bound, consts, *args,
      has_loop_index=has_loop_index, step=1, bound_type=bound_type)
  if has_loop_index:
    # Need to return the final loop index value if the outer scan expects
    # it as an output
    return [upper_bound, *for_out]
  return for_out

