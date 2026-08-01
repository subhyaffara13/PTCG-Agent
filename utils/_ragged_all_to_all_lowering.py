
def _ragged_all_to_all_lowering(
    ctx, operand, output, input_offsets, send_sizes, output_offsets, recv_sizes,
    *, axis_name, axis_index_groups
):
  replica_groups = _replica_groups(ctx.module_context.axis_context, axis_name,
                                   axis_index_groups)

  # Assumes all groups are the same size
  split_count = len(replica_groups[0])
  if not all(split_count == len(g) for g in replica_groups):
    raise ValueError('Replica groups must be equally sized')

  ragged_all_to_all_attrs: dict[str, ir.Attribute] = {
      "replica_groups": _replica_groups_hlo(replica_groups)
  }
  is_spmd = isinstance(
      ctx.module_context.axis_context, (SPMDAxisContext, ShardingContext))
  if is_spmd:
    ragged_all_to_all_attrs['channel_id'] = ir.IntegerAttr.get(
        ir.IntegerType.get_signless(64), mlir.COLLECTIVE_CHANNEL_ID
    )

  return hlo.CustomCallOp(
      result=[output.type],
      inputs=[operand, output, input_offsets, send_sizes, output_offsets,
              recv_sizes],
      call_target_name=ir.StringAttr.get('ragged_all_to_all'),
      backend_config=ir.DictAttr.get(ragged_all_to_all_attrs),
      api_version=ir.IntegerAttr.get(ir.IntegerType.get_signless(32), 4),
  ).results

