
def _atomic_rmw(
    op: tt_dialect.RMWOp,
    ptr: ir.Value,
    val: ir.Value,
    mask: ir.Value | None = None,
    semantic: tt_dialect.MemSemantic = tt_dialect.MemSemantic.ACQUIRE_RELEASE,
    sync_scope: tt_dialect.MemSyncScope = tt_dialect.MemSyncScope.GPU,
) -> ir.Value:
  if isinstance(ptr.type, ir.RankedTensorType):
    ptr_type = ir.RankedTensorType(ptr.type)
    element_type = tt_dialect.PointerType(ptr_type.element_type)
    result_type = ir.RankedTensorType.get(
        ptr_type.shape, element_type.pointee_type, ptr_type.encoding
    )
  else:
    result_type = tt_dialect.PointerType(ptr.type).pointee_type
  return tt_dialect.atomic_rmw(
      result_type, op, ptr, val, mask=mask, sem=semantic, scope=sync_scope
  )


def _atomic_rmw(
    x_ref_or_view,
    idx,
    val,
    *,
    mask: Any | None = None,
    atomic_type: AtomicOpType,
):
  x_ref, transforms = state_primitives.get_ref_and_transforms(
      x_ref_or_view, idx, "atomic_rmw"
  )
  args_flat, args_tree = tree_util.tree_flatten((x_ref, transforms, val, mask))
  return atomic_rmw_p.bind(
      *args_flat, args_tree=args_tree, atomic_type=atomic_type
  )

