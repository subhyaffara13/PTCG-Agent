
def _lower_while_via_fori(
    ctx: LoweringRuleContext,
    *args,
    fori_jaxpr,
    cond_nconsts,
    cond_jaxpr,
    body_nconsts,
    body_jaxpr,
):
  _, body_consts, carry = split_list(args, [cond_nconsts, body_nconsts])
  (lb, ub), args = carry[:2], carry[2:]
  for_out = _lower_jaxpr_to_for_loop(
      ctx.replace(
          block_shapes=(
              *ctx.block_shapes[: body_nconsts + 1],
              *ctx.block_shapes[body_nconsts + 2 :],
          ),
      ),
      fori_jaxpr,
      lb,
      arith.subi(ub, lb),
      body_consts,
      *args,
      has_loop_index=True,
      unroll=1,
  )
  return [ub, ub, *for_out]


def _lower_while_via_fori(
    ctx: LoweringRuleContext,
    *args,
    fori_jaxpr,
    cond_nconsts,
    body_nconsts,
):
  assert not fori_jaxpr.constvars
  # The pattern matcher looks for conditions with no constants.
  assert cond_nconsts == 0

  # Reflect the changes of the pattern matcher to the context.
  lb_aval, ub_aval, *_ = ctx.avals_in[cond_nconsts + body_nconsts:]
  ctx = ctx.replace(
      avals_in=(
          *ctx.avals_in[cond_nconsts:body_nconsts],
          ctx.avals_in[body_nconsts],  # the index
          *ctx.avals_in[body_nconsts + 2 :],
      ),
      avals_out=tuple(ctx.avals_out[2:]),
  )
  _, consts, (lb, ub, *args) = util.split_list(
      args, [cond_nconsts, body_nconsts]
  )
  lb = _ensure_ir_value(lb, lb_aval.dtype)
  ub = _ensure_ir_value(ub, ub_aval.dtype)
  for_out = _lower_jaxpr_to_for_loop(
      ctx,
      fori_jaxpr,
      lb,
      arith_dialect.subi(ub, lb),
      consts,
      *args,
      has_loop_index=True,
  )
  return ub, ub, *for_out

