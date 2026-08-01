
def transform_array(x, transforms):
  if transforms is None:
    transforms = []
  result = x
  for transform in transforms:
    if transform is None:
      continue
    match transform:
      case indexing.NDIndexer():
        result = _index_array(result, transform)
      case BitcastTransform():
        result = bitcast(result, transform.dtype)
      case ReshapeTransform():
        result = result.reshape(transform.shape)
      case _:
        raise NotImplementedError(f"Unsupported transform: {transform}")
  return result

