
def _allreduce_lowering(prim, pos_fn, ctx, arg, *, axes, axis_index_groups):
  aval_in, = ctx.avals_in
  if axis_index_groups is not None and ("tpu" in ctx.module_context.platforms):
    len_0 = len(axis_index_groups[0])
    if any(len(g) != len_0 for g in axis_index_groups):
      raise ValueError("axis_index_groups must all be the same size for TPU lowering")
  named_axes, positional_axes = axes_partition = [], []
  for axis in axes:
    axes_partition[isinstance(axis, int)].append(axis)

  if positional_axes:
    reducer = mlir.lower_fun(pos_fn, multiple_results=False)
    def _positional_reduce(aval, arg):
      aval_out = aval.update(
          shape=np.delete(np.array(aval.shape, dtype=np.int64),
                          positional_axes))
      reducer_ctx = ctx.replace(primitive=None, avals_in=[aval], avals_out=[aval_out])
      out, = reducer(reducer_ctx, arg, axes=tuple(positional_axes))
      return out
    arg = _positional_reduce(aval_in, arg)
  if not named_axes:
    return [arg]

  replica_groups = _replica_groups_hlo(
      _replica_groups(ctx.module_context.axis_context, named_axes,
                      axis_index_groups))
  axis_context = ctx.module_context.axis_context
  is_spmd = isinstance(axis_context, (SPMDAxisContext, ShardingContext))

  def all_reduce(aval, x):
    if is_spmd:
      other_args: dict[str, Any] = dict(
          channel_handle=hlo.ChannelHandle.get(
              mlir.COLLECTIVE_CHANNEL_ID, mlir.DEVICE_TO_DEVICE_TYPE),
          use_global_device_ids=ir.BoolAttr.get(True))
    else:
      other_args = {}

    op = hlo.AllReduceOp(
        [x.type], [x], replica_groups=replica_groups, **other_args)
    scalar_aval = core.ShapedArray(
        (), aval.dtype, sharding=NamedSharding(aval.sharding.mesh, P()))
    scalar_type = mlir.aval_to_ir_type(ctx.module_context, scalar_aval)
    reducer_block = op.regions[0].blocks.append(scalar_type, scalar_type)
    with ir.InsertionPoint(reducer_block):
      lower_reducer = mlir.lower_fun(prim.bind, multiple_results=False)
      reducer_ctx = ctx.replace(primitive=None,
                                avals_in=[scalar_aval] * 2, avals_out=[scalar_aval])
      out_nodes = lower_reducer(reducer_ctx, *reducer_block.arguments)
      flat_out_nodes, _ = mlir.ir_tree_registry.flatten(out_nodes)
      hlo.return_(flat_out_nodes)
    return op.result
  return [all_reduce(aval_in, arg)]

