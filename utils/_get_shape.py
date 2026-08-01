
def _get_shape(t):
    return getattr(t, "shape", None)


def _get_shape(
    arr: AbstractArrayLike | AbstractArrayLikeGlobalShape,
) -> types.Shape:
  if hasattr(arr, 'shape'):
    return arr.shape
  if hasattr(arr, 'global_shape'):
    return arr.global_shape
  raise ValueError(f'Object does not have a `shape` property: {arr}')

