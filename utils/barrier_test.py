
def barrier_test(barrier: state.AbstractRef) -> jax.Array:
  """Tests the given barrier.

  This is a non-blocking equivalent of `barrier_wait`, which returns a boolean
  indicating whether or not the current barrier phase is complete.

  `barrier_test` is only supported within a warp context.
  """
  barrier, transforms = state_primitives.get_ref_and_transforms(
      barrier, None, "barrier_test"
  )
  flat_transforms, transforms_treedef = tree_util.tree_flatten(transforms)
  return barrier_test_p.bind(
      barrier, *flat_transforms, transforms_treedef=transforms_treedef,
  )

