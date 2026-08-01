
def _atomic_store_abstract_eval(*avals_flat, args_tree, atomic_type):
  del atomic_type
  ref, transforms, val = args_tree.unflatten(avals_flat)
  if transforms is not None:
    ref = pallas_core.TransformedRef(ref, transforms)
  if ref.shape != val.shape:
    raise ValueError(
        f"Invalid shape for `swap`. Ref shape: {ref.shape}. "
        f"Value shape: {val.shape}."
    )
  if ref.dtype != val.dtype:
    raise ValueError(
        f"Invalid dtype for `swap`. Ref dtype: {ref.dtype}. "
        f"Value dtype: {val.dtype}."
    )
  return (), {state.WriteEffect(0)}

