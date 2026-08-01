
def _while_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    cond_nconsts,
    cond_jaxpr,
    body_nconsts,
    body_jaxpr,
):
  # First try to lower via a simpler fori loop, which may optimize better.
  fori_jaxpr, _ = pallas_utils.pattern_match_while_to_fori_loop(
      cond_jaxpr, cond_nconsts, body_jaxpr, body_nconsts
  )
  if fori_jaxpr is not None:
    return _lower_while_via_fori(
        ctx,
        *args,
        fori_jaxpr=fori_jaxpr,
        cond_nconsts=cond_nconsts,
        cond_jaxpr=cond_jaxpr,
        body_nconsts=body_nconsts,
        body_jaxpr=body_jaxpr,
    )

  # If we fail conversion to fori, fallback to an ordinary while loop.
  cond_consts, body_consts, carry = split_list(
      args, [cond_nconsts, body_nconsts]
  )
  cond_const_block_shapes, body_const_block_shapes, carry_block_shapes = (
      split_list(ctx.block_shapes, [cond_nconsts, body_nconsts])
  )
  carry_types = [a.type for a in carry]
  while_op = scf.WhileOp(carry_types, carry)

  before_block = while_op.before.blocks.append(*carry_types)
  with ir.InsertionPoint.at_block_begin(before_block):
    cond_args = [*cond_consts, *before_block.arguments]
    [cond] = jaxpr_subcomp(
        ctx.lowering_context.replace(
            block_shapes=[*cond_const_block_shapes, *carry_block_shapes]
        ),
        cond_jaxpr.jaxpr,
        *cond_args,
    )
    scf.condition(cond, before_block.arguments)

  after_block = while_op.after.blocks.append(*carry_types)
  with ir.InsertionPoint.at_block_begin(after_block):
    body_args = [*body_consts, *after_block.arguments]
    loop_out = jaxpr_subcomp(
        ctx.lowering_context.replace(
            block_shapes=[*body_const_block_shapes, *carry_block_shapes],
        ),
        body_jaxpr.jaxpr,
        *body_args,
    )
    if loop_out:
      scf.yield_(loop_out)
  return list(while_op.results)


def _while_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    cond_jaxpr,
    body_jaxpr,
    cond_nconsts,
    body_nconsts,
):
  # First try to lower via a simpler fori loop, which may optimize better.
  fori_jaxpr, _ = pallas_utils.pattern_match_while_to_fori_loop(
      cond_jaxpr, cond_nconsts, body_jaxpr, body_nconsts
  )
  if fori_jaxpr is not None:
    return _lower_while_via_fori(
        ctx,
        *args,
        fori_jaxpr=fori_jaxpr,
        cond_nconsts=cond_nconsts,
        body_nconsts=body_nconsts,
    )

  _is_acc = lambda x: isinstance(x, mgpu.WGMMAAccumulator)
  _ensure = _ensure_ir_value
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    _ensure = lambda v, aval: v if _is_acc(v) else _ensure_fa(v, aval.dtype)

  # If we fail conversion to fori, fallback to an ordinary while loop.
  cond_consts, body_consts, carry = util.split_list(
      args, [cond_nconsts, body_nconsts]
  )
  _cond_avals, _body_avals, carry_avals = util.split_list(
      ctx.avals_in, [cond_nconsts, body_nconsts]
  )
  carry = [*map(_ensure, carry, carry_avals)]
  # Flatten the carry to get a concatenated list of registers from each FA.
  # Note that the treedef is also used below to unflatten the body results.
  flat_carry, carry_treedef = jax.tree.flatten(carry)
  flat_carry_types = [a.type for a in flat_carry]
  while_op = scf_dialect.WhileOp(flat_carry_types, flat_carry)

  before_block = while_op.before.blocks.append(*flat_carry_types)
  with ir.InsertionPoint.at_block_begin(before_block):
    cond_args = [*cond_consts, *carry_treedef.unflatten(before_block.arguments)]
    [cond] = lower_jaxpr_to_mosaic_gpu(
        ctx.module_ctx, ctx.launch_ctx, cond_jaxpr.jaxpr, cond_args
    )
    scf_dialect.condition(
        _ensure_ir_value(cond, *cond_jaxpr.out_avals), before_block.arguments
    )

  after_block = while_op.after.blocks.append(*flat_carry_types)
  with ir.InsertionPoint.at_block_begin(after_block):
    body_args = [*body_consts, *carry_treedef.unflatten(after_block.arguments)]
    loop_out = lower_jaxpr_to_mosaic_gpu(
        ctx.module_ctx, ctx.launch_ctx, body_jaxpr.jaxpr, body_args
    )
    loop_out = [*map(_ensure, loop_out, carry_avals)]
    if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
      for idx, (carry_fa, out_fa) in enumerate(zip(carry, loop_out)):
        if _is_acc(carry_fa) != _is_acc(out_fa):
          raise ValueError(
              f"The loop body output has unexpected accumulator type:"
              f" output[{idx}] is {out_fa}, when it should be {carry_fa}."
          )

        if not _is_acc(out_fa) and carry_fa.layout != out_fa.layout:
          raise ValueError(
              f"The loop body output has unexpected layout: output[{idx}] has"
              f" layout {out_fa.layout}, when it should be {carry_fa.layout}."
          )
    scf_dialect.yield_(
        carry_treedef.flatten_up_to(loop_out) if loop_out else []
    )
  return carry_treedef.unflatten(list(while_op.results))


def _while_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    cond_nconsts,
    cond_jaxpr,
    body_nconsts,
    body_jaxpr,
):
  args = map(_ensure_ir_value, args, ctx.avals_in)

  # First, try to pattern match to fori_loop and lower to scf.for if possible
  # TODO(slebedev): Use `pallas_utils.pattern_match_while_to_fori_loop`.
  result = _maybe_pattern_match_fori_loop(ctx, *args, cond_nconsts=cond_nconsts,
                                          body_nconsts=body_nconsts, cond_jaxpr=cond_jaxpr,
                                          body_jaxpr=body_jaxpr)
  if result is not None:
    return result
  # Fall back to default while lowering
  cond_consts, body_consts, carry = util.split_list(
      args, [cond_nconsts, body_nconsts]
  )
  cond_const_block_infos, body_const_block_infos, carry_block_infos = (
      util.split_list(ctx.block_infos, [cond_nconsts, body_nconsts])
  )
  cond_const_types = [a.type for a in cond_consts]
  body_const_types = [a.type for a in body_consts]
  carry_types = [a.type for a in carry]
  all_types = [*cond_const_types, *body_const_types, *carry_types]
  while_op = scf_dialect.WhileOp(all_types, args)

  before_block = while_op.before.blocks.append(*all_types)
  cond_consts_, _, carry_ = util.split_list(
      before_block.arguments,
      [cond_nconsts, body_nconsts],
  )
  cond_args = [*cond_consts_, *carry_]
  with ir.InsertionPoint.at_block_begin(before_block):
    [cond] = lower_jaxpr_to_triton_ir(
        ctx.context,
        cond_jaxpr.jaxpr,
        [*cond_const_block_infos, *carry_block_infos],
        *cond_args,
    )
    scf_dialect.condition(cond, before_block.arguments)

  after_block = while_op.after.blocks.append(*all_types)
  cond_consts_, body_consts_, carry_ = util.split_list(
      after_block.arguments,
      [cond_nconsts, body_nconsts],
  )
  all_args = [*cond_consts_, *body_consts_, *carry_]
  cond_const_args, body_const_args, carry_args = util.split_list(
      all_args, [cond_nconsts, body_nconsts]
  )
  with ir.InsertionPoint.at_block_begin(after_block):
    loop_out = lower_jaxpr_to_triton_ir(
        ctx.context,
        body_jaxpr.jaxpr,
        [*body_const_block_infos, *carry_block_infos],
        *body_const_args,
        *carry_args
    )
    all_handles = [*cond_const_args, *body_const_args, *loop_out]
    if all_handles:
      scf_dialect.yield_(all_handles)

  all_out = list(while_op.results_)
  return all_out[cond_nconsts + body_nconsts :]

