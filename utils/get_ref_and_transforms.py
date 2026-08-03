from typing import Any

def get_ref_and_transforms(
    ref_or_view: Any,
    idx: Indexer | tuple[Indexer, ...] | None,
    function_name: str,
) -> tuple[Any, tuple[Transform, ...]]:
  if isinstance(ref_or_view, TransformedRef):
    ref, transforms = ref_or_view.ref, ref_or_view.transforms
  else:
    ref, transforms = ref_or_view, ()
  ref_aval = core.typeof(ref)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"Can only call `{function_name}` on a `Ref`: {ref}.")
  if (not isinstance(ref_aval.inner_aval, core.ShapedArray)
      and not ref_aval.inner_aval.is_high):
    return ref, ()

  if idx is None or idx is Ellipsis:
    idx = ()
  elif not isinstance(idx, tuple):
    idx = (idx,)

  if not idx:
    return ref, transforms
  if not idx and transforms and isinstance(transforms[-1], indexing.NDIndexer):
    return ref, transforms
  nd_indexer = indexing.NDIndexer.from_indices_shape(idx, ref_or_view.shape)
  return ref, (*transforms, nd_indexer)

