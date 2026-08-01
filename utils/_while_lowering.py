
def _while_lowering(ctx, *args, cond_jaxpr, body_jaxpr, cond_nconsts,
                    body_nconsts):
  pred_aval = cond_jaxpr.out_avals[0]
  batched = bool(pred_aval.shape)
  cond_ordered_effects = effects.ordered_effects.filter_in(cond_jaxpr.effects)
  if cond_ordered_effects:
    def cond(args):
      # Pred can be batched
      pred = core.eval_jaxpr(cond_jaxpr.jaxpr, cond_jaxpr.consts, *args)[0]
      if batched:
        pred = lax.reduce_or(pred, tuple(range(len(pred_aval.shape))))
      return pred
    def body(args):
      return core.eval_jaxpr(body_jaxpr.jaxpr, body_jaxpr.consts, *args)
    def new_cond(pred_args):
      pred, *_ = pred_args
      return pred
    def new_body(pred_args):
      _, cond_consts, body_consts, carry = pred_args
      carry = body((*body_consts, *carry))
      pred = cond((*cond_consts, *carry))
      return pred, cond_consts, body_consts, carry
    def fun(*args):
      cond_consts, body_consts, carry = split_list(args, [cond_nconsts, body_nconsts])
      pred = cond((*cond_consts, *carry))
      *_, out = while_loop(new_cond, new_body, (pred, cond_consts, body_consts, carry))
      return out
    return mlir.lower_fun(fun)(ctx, *args)

  loop_carry_types = _map(partial(mlir._aval_to_ir_types, ctx.module_context), ctx.avals_in)
  body_effects = effects.ordered_effects.filter_in(body_jaxpr.effects)
  num_tokens = len(body_effects)
  tokens = [ctx.tokens_in.get(eff) for eff in body_effects]
  token_types = [mlir.token_type() for _ in tokens]
  loop_carry_types = [*token_types, *loop_carry_types]
  flat_loop_carry_types, loop_carry_treedef = mlir.ir_tree_registry.flatten(loop_carry_types)
  args = [*tokens, *args]

  flat_args, _ = mlir.ir_tree_registry.flatten(args)
  while_op = hlo.WhileOp(flat_loop_carry_types, flat_args)

  # Loop condition
  cond_block = while_op.regions[0].blocks.append(*flat_loop_carry_types)
  name_stack = ctx.name_stack.extend('while')
  with ir.InsertionPoint(cond_block):
    flat_cond_args = [
        cond_block.arguments[i] for i in range(len(flat_loop_carry_types))
    ]
    cond_args = loop_carry_treedef.unflatten(flat_cond_args)
    cond_args = cond_args[num_tokens:]  # Remove tokens from cond args
    x, _, z = util.split_list(cond_args, [cond_nconsts, body_nconsts])
    cond_consts = mlir.ir_consts(
        cond_jaxpr.consts, [v.aval for v in cond_jaxpr.jaxpr.constvars])
    cond_name_stack = name_stack.extend('cond')
    (pred,), _ = mlir.jaxpr_subcomp(
        ctx.module_context,
        cond_jaxpr.jaxpr,
        cond_name_stack,
        mlir.TokenSet(),
        cond_consts,
        *(x + z),
        dim_var_values=ctx.dim_var_values,
        const_lowering=ctx.const_lowering,
        outer_traceback=ctx.traceback,
    )
    if batched:
      pred_ctx = mlir.LoweringRuleContext(
          module_context=ctx.module_context,
          name_stack=cond_name_stack,
          traceback=ctx.traceback,
          primitive=None,
          avals_in=[pred_aval],
          avals_out=[pred_aval.update(
              shape=(), sharding=pred_aval.sharding.update(spec=()))],
          tokens_in=mlir.TokenSet(),
          tokens_out=None,
          dim_var_values=ctx.dim_var_values,
          const_lowering=ctx.const_lowering)
      pred, = lax._unary_reduce_lower(
          hlo.OrOp,
          lambda dtype: np.array(False, dtype),
          pred_ctx,
          pred,
          axes=tuple(range(len(pred_aval.shape))))
    flat_pred, _ = mlir.ir_tree_registry.flatten([pred])
    hlo.return_(flat_pred)

  # Loop body
  body_block = while_op.regions[1].blocks.append(*flat_loop_carry_types)
  with ir.InsertionPoint(body_block):
    flat_body_args = [
        body_block.arguments[i] for i in range(len(flat_loop_carry_types))
    ]
    body_args = loop_carry_treedef.unflatten(flat_body_args)
    # Tokens are at the front of the args list to the while loop
    token_args, body_args = util.split_list(body_args, [num_tokens])
    tokens_in = mlir.TokenSet(dict(zip(body_effects, token_args)))
    x, y, z = util.split_list(body_args, [cond_nconsts, body_nconsts])
    body_name_stack = name_stack.extend('body')
    body_consts = mlir.ir_consts(
        body_jaxpr.consts, [v.aval for v in body_jaxpr.jaxpr.constvars])
    new_z, tokens_out = mlir.jaxpr_subcomp(
        ctx.module_context, body_jaxpr.jaxpr, body_name_stack,
        tokens_in, body_consts, *(y + z),
        dim_var_values=ctx.dim_var_values, const_lowering=ctx.const_lowering,
        outer_traceback=ctx.traceback)
    out_tokens = [tokens_out.get(eff) for eff in body_effects]
    if batched:
      body_pred_name_stack = name_stack.extend('body_pred')
      cond_consts = mlir.ir_consts(
          cond_jaxpr.consts, [v.aval for v in cond_jaxpr.jaxpr.constvars])
      (body_pred,), _ = mlir.jaxpr_subcomp(
          ctx.module_context, cond_jaxpr.jaxpr, body_pred_name_stack,
          mlir.TokenSet(), cond_consts, *(x + z),
          dim_var_values=ctx.dim_var_values, const_lowering=ctx.const_lowering,
          outer_traceback=ctx.traceback)
      new_z = _map(
          partial(_pred_bcast_select_hlo, ctx, pred_aval, body_pred), new_z, z,
          body_jaxpr.out_avals)

    flat_out, _ = mlir.ir_tree_registry.flatten([out_tokens, x, y, new_z])
    hlo.return_(flat_out)

  outputs = loop_carry_treedef.unflatten(while_op.results)
  tokens, _, _, z = util.split_list(outputs, [num_tokens, cond_nconsts, body_nconsts])
  z = [mlir.lower_with_sharding_in_types(ctx, op, aval)
       for op, aval in zip(z, ctx.avals_out)]
  if tokens:
    ctx.set_tokens_out(mlir.TokenSet(dict(zip(body_effects, tokens))))
  return z

