
def _transform_ref(ref, ref_ty, ref_block_shape, transforms=()):
  # Unwrap the refs if they are TransformedRefs.
  if transforms == () and isinstance(ref, state.TransformedRef):
    ref, transforms = _get_ref_and_transforms(ref)
  if isinstance(ref_ty, state.TransformedRef):
    ref_ty, _ = _get_ref_and_transforms(ref_ty)
  if isinstance(ref_block_shape, state.TransformedRef):
    ref_block_shape, _ = _get_ref_and_transforms(ref_block_shape)
  assert not isinstance(ref_ty, state.TransformedRef)
  assert not isinstance(ref_block_shape, state.TransformedRef)
  for transform in transforms:
    match transform:
      case NDIndexer():
        ref, ref_block_shape = _slice_memref(
            ref, transform, ref_ty, ref_block_shape
        )
      case state_types.BitcastTransform():
        ref, ref_block_shape = _bitcast_memref(
            ref, transform, ref_ty, ref_block_shape
        )
      case state_types.ReshapeTransform():
        ref, ref_block_shape = _reshape_memref(
            ref, transform, ref_ty, ref_block_shape
        )
      case state_types.SelectTransform():
        raise NotImplementedError(
            "_transform_ref() only supports single ref transforms. Got:"
            f" {ref = }, {ref_ty = }, {ref_block_shape = }, {transforms = }"
        )
      case _:
        raise NotImplementedError(f"Unsupported transform: {transform}")
    ref_ty = transform.transform_type(ref_ty)
  return ref, ref_block_shape

