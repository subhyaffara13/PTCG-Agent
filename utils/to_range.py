
def to_range(transforms) -> tuple[slice | int, ...]:
  ret = ()
  for transform in transforms:
    # For now, assume only NDIndexer transforms.
    ret = _compose_slice_or_index(
        ret, tuple(_transform_slice_or_index(i) for i in transform.indices)
    )
  return ret

