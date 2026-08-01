
def _atomic_store(
    x_ref_or_view,
    val,
    *,
    atomic_type: AtomicOpType,
):
  x_ref, transforms = state_primitives.get_ref_and_transforms(
      x_ref_or_view, None, "atomic_store"
  )
  args_flat, args_tree = tree_util.tree_flatten((x_ref, transforms, val))
  atomic_store_p.bind(
      *args_flat, args_tree=args_tree, atomic_type=atomic_type
  )

