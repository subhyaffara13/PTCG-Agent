
def _addupdate_lowering_rule(ctx: LoweringRuleContext, ptr, value, *idx, tree):
  block_info, *_ = ctx.block_infos
  assert block_info is not None
  indexers = tree_util.tree_unflatten(tree, idx)
  if not _is_triton_pointer_type(ptr.type):
    assert len(indexers) == 0
    return ptr
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  indexer = indexers[0]
  ptr = _compute_pointers_from_indices(ptr, block_info, indexer)
  op = tt_dialect.RMWOp.FADD
  if isinstance(_element_type(value.type), ir.IntegerType):
    op = tt_dialect.RMWOp.ADD
  _atomic_rmw(op, ptr, value)
  return []

