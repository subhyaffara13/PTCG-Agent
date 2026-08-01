
def _cond_lowering(ctx, index, *args, branches, **params):
  if (branches_platforms := params.get("branches_platforms", None)) is not None:
    branches_kept: list[core.ClosedJaxpr] = []
    index_to_kept_index: dict[int, int] = {}
    for p in mlir._platforms_for_eqn(ctx):
      # Each `p` must appear in exactly one branches_platforms, or in the
      # last default branch. Otherwise, platform_index lowering would have
      # failed already.
      for b_idx, b_platforms in enumerate(branches_platforms):
        if b_platforms is None or p in b_platforms:
          if b_idx not in index_to_kept_index:
            index_to_kept_index[b_idx] = len(branches_kept)
            branches_kept.append(branches[b_idx])
          break
      else:
        assert False, p

    # Compute the new index into branches_keep
    i32_type = ir.RankedTensorType.get([], mlir.dtype_to_ir_type(dtypes.dtype(np.int32)))
    kept_index_case_op = hlo.CaseOp([i32_type],
                                    index=index,
                                    num_branches=len(branches))
    for i in range(len(branches)):
      branch = kept_index_case_op.regions[i].blocks.append()
      with ir.InsertionPoint(branch):
        kept_i = np.int32(index_to_kept_index.get(i, 0))
        hlo.return_([mlir.ir_constant(kept_i)])

    index = kept_index_case_op
    branches = branches_kept
    assert branches, "platform_index lowering should have failed first"

  joined_effects = core.join_effects(*(branch.effects for branch in branches))
  ordered_effects = list(effects.ordered_effects.filter_in(joined_effects))
  num_tokens = len(ordered_effects)
  tokens_in = ctx.tokens_in.subset(ordered_effects)
  output_token_types = [mlir.token_type() for _ in ordered_effects]
  output_types = [
      *output_token_types, *map(partial(mlir._aval_to_ir_types, ctx.module_context), ctx.avals_out)]
  flat_output_types, treedef = mlir.ir_tree_registry.flatten(output_types)

  # CaseOp takes a single argument 'index' and the corresponding blocks
  # have no arguments; the computation within the block uses implicit
  # captures.
  case_op = hlo.CaseOp(flat_output_types, index=index,
                       num_branches=len(branches))
  name_stack = ctx.name_stack.extend('cond')
  for i, jaxpr in enumerate(branches):
    branch = case_op.regions[i].blocks.append()
    with ir.InsertionPoint(branch):
      consts = mlir.ir_consts(
          jaxpr.consts, [v.aval for v in jaxpr.jaxpr.constvars])
      out_vals, tokens_out = mlir.jaxpr_subcomp(
          ctx.module_context, jaxpr.jaxpr, name_stack.extend(f'branch_{i}_fun'),
          tokens_in, consts, *args,
          dim_var_values=ctx.dim_var_values, const_lowering=ctx.const_lowering,
          outer_traceback=ctx.traceback)
      out_tokens = [tokens_out.get(eff) for eff in ordered_effects]
      out_vals = [*out_tokens, *out_vals]
      flat_out_vals, _ = mlir.ir_tree_registry.flatten(out_vals)
      hlo.return_(flat_out_vals)

  tokens_and_outputs = treedef.unflatten(case_op.results)
  tokens, outputs = util.split_list(tokens_and_outputs, [num_tokens])
  outputs = [mlir.lower_with_sharding_in_types(ctx, o, aval)
             for o, aval in zip(outputs, ctx.avals_out)]
  ctx.set_tokens_out(mlir.TokenSet(dict(zip(ordered_effects, tokens))))
  return outputs

