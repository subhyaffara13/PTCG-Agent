
def _cond_lowering_rule(ctx: LoweringRuleContext, *args, branches, **params):
  index, *args = args
  constant_index = _fold_and_get_constant_value(index)

  if constant_index is not None:
    return jaxpr_subcomp(
        ctx.lowering_context.replace(block_shapes=ctx.block_shapes[1:]), branches[constant_index].jaxpr, *args
    )
  out_types = map(ctx.aval_to_ir_type, ctx.avals_out)
  pred = arith.cmpi(
      arith.CmpIPredicate.ne, index, ir_constant(0, index.type)
  )
  if_op = scf.IfOp(pred, out_types, has_else=True)
  lowering_context = ctx.lowering_context.replace(
      block_shapes=ctx.block_shapes[1:],
  )
  with ir.InsertionPoint(if_op.then_block):
    # TODO(b/300272065): Use `scf.IndexSwitchOp` instead of a cascade of
    # if/else.
    if len(branches) > 2:
      out = _cond_lowering_rule(
          ctx,
          arith.subi(index, ir_constant(1, index.type)),
          *args,
          branches=branches[1:],
      )
    else:
      out = jaxpr_subcomp(lowering_context, branches[1].jaxpr, *args)
    scf.yield_(out)
  assert if_op.else_block is not None
  with ir.InsertionPoint(if_op.else_block):
    out = jaxpr_subcomp(lowering_context, branches[0].jaxpr, *args)
    scf.yield_(out)
  return if_op.results


def _cond_lowering_rule(ctx: LoweringRuleContext, index, *args, branches,
                        **params):
  if params:
    raise NotImplementedError("platform_dependent cond")
  index_aval, *_arg_avals = ctx.avals_in

  _is_acc = lambda x: isinstance(x, mgpu.WGMMAAccumulator)
  _ensure = _ensure_ir_value
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    _ensure = lambda v, aval: v if _is_acc(v) else _ensure_fa(v, aval.dtype)

  def _yielded_values(outs, avals):
    return [*map(_ensure, outs, avals)]

  # We need to know the result types ahead of time to construct the switch
  # operation. Below we lower the first branch in a throw-away module to
  # extract them.
  tmp_module = ir.Module.create()
  # The module attributes are needed for `get_arch` to work correctly.
  for k, v in ctx.launch_ctx.module.operation.attributes.items():
    tmp_module.operation.attributes[k] = v

  with ir.InsertionPoint(tmp_module.body):
    outs = lower_jaxpr_to_mosaic_gpu(
        ctx.module_ctx, ctx.launch_ctx, branches[0].jaxpr, args
    )
    yielded_types = [
        v.type for v in jax.tree.leaves(_yielded_values(outs, ctx.avals_out))
    ]
    del outs

  switch_op = scf_dialect.IndexSwitchOp(
      yielded_types,
      _as_index(_ensure_ir_value(index, index_aval.dtype)),
      range(len(branches) - 1),
  )

  # ``RegionSequence`` in MLIR does not support slicing, so the
  # auto-generated Python bindings for ``caseRegions`` fail at runtime!
  # We convert it to a list to work around that.
  regions = list(switch_op.regions)
  # Move the default region to the back.
  regions = regions[1:] + regions[:1]
  treedef: tree_util.PyTreeDef | None = None
  for branch, region in zip(branches, regions):
    block = region.blocks[0]
    with ir.InsertionPoint(block):
      outs = lower_jaxpr_to_mosaic_gpu(
          ctx.module_ctx, ctx.launch_ctx, branch.jaxpr, args, consts=branch.consts
      )

      yielded_leaves, yielded_treedef = jax.tree.flatten(_yielded_values(outs, ctx.avals_out))
      if treedef is None:
        treedef = yielded_treedef
      else:
        assert treedef == yielded_treedef

      scf_dialect.yield_(yielded_leaves)

  assert treedef is not None
  return treedef.unflatten(list(switch_op.results))


def _cond_lowering_rule(
    ctx: LoweringRuleContext,
    index,
    *args,  # *consts, *ops
    branches,  # tuple(jaxprs)
):
  block_infos = ctx.block_infos

  def to_type(out_aval):
    element_type = _dtype_to_ir_type(out_aval.dtype)
    if not out_aval.shape:
      return element_type
    return ir.RankedTensorType.get(out_aval.shape, element_type)

  out_types = [to_type(out) for out in ctx.avals_out]

  use_branch0 = _equal(index, _ir_constant(0, index.type), signed=False)
  # TODO(bjp): Switch to scf.index_switch once exposed in triton.cc
  if_op = scf_dialect.IfOp(use_branch0, out_types, has_else=True)
  with ir.InsertionPoint.at_block_begin(if_op.then_block):
    outs0 = lower_jaxpr_to_triton_ir(
        ctx.context,
        branches[0].jaxpr,
        block_infos[1:],
        *args)
    scf_dialect.yield_(outs0)
  assert if_op.else_block is not None
  with ir.InsertionPoint.at_block_begin(if_op.else_block):
    # TODO(bjp): Instead of linear nest of 'if's, partition into halves.
    if len(branches) > 2:
      outs1 = _cond_lowering_rule(
          ctx,
          _sub(index, _ir_constant(1, index.type)),
          *args,
          branches=branches[1:],
      )
    else:
      outs1 = lower_jaxpr_to_triton_ir(
          ctx.context,
          branches[1].jaxpr,
          block_infos[1:],
          *args)
    scf_dialect.yield_(outs1)

  return list(if_op.results_)

