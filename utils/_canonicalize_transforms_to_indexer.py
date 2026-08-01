
def _canonicalize_transforms_to_indexer(
      ref_aval,
      transforms,
      transforms_avals,
):
  if not transforms:
    prev_transforms, idx = [], NDIndexer.make_trivial_indexer(ref_aval.shape)
  else:
    if not isinstance(transforms[-1], NDIndexer):
      new_ref_aval = state.transform_type(transforms, ref_aval)
      assert isinstance(new_ref_aval, state.AbstractRef)
      idx = NDIndexer.make_trivial_indexer(new_ref_aval.shape)
      prev_transforms = transforms
    else:
      (*prev_transforms, idx) = transforms
      (*_, idx_aval) = transforms_avals
      if any(
          (not isinstance(a, primitives.Slice) and a.shape)
          for a in idx_aval.indices
      ):
        raise ValueError("Cannot do int indexing on TPU")
  return prev_transforms, idx

