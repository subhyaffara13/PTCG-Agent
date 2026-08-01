
def barrier_wait(barrier: state.AbstractRef) -> None:
  """Waits on the given barrier."""
  barrier, transforms = state_primitives.get_ref_and_transforms(
      barrier, None, "barrier_wait"
  )
  flat_transforms, transforms_treedef = tree_util.tree_flatten(transforms)
  barrier_wait_p.bind(
      barrier, *flat_transforms, transforms_treedef=transforms_treedef,
  )

