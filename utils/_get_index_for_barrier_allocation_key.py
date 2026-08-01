
def _get_index_for_barrier_allocation_key(
    transforms_treedef, transforms_leaves,
) -> indexing.DimIndexer | None:
  # TODO(nrink): The working out of `transforms` and the returned index below
  # may need tidying up. Specifically, GPU interpret mode should correctly
  # support legal ways to index into barriers. (Here, 'legal' is to be read as
  # 'allowed by the Pallas GPU semantics'.)
  transforms = jax.tree.unflatten(transforms_treedef, transforms_leaves)

  if not transforms:
    return None
  if not hasattr(transforms, "__len__") or len(transforms) != 1:
    raise NotImplementedError(
        f"Indexing barrier with {transforms} not supported in GPU interpret"
        " mode"
    )
  if not isinstance(transforms[0], indexing.NDIndexer):
    raise ValueError(f"Expected an `NDIndexer`, but got {transforms[0]}")
  if len(transforms[0].indices) != 1:
    raise ValueError(
        f"Expected a singleton index, but got {transforms[0].indices}"
    )
  return transforms[0].indices[0]

