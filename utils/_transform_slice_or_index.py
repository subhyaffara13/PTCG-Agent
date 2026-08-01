
def _transform_slice_or_index(slice_or_idx):
  if isinstance(slice_or_idx, int):
    return slice_or_idx
  else:
    start = int(slice_or_idx.start)
    size = int(slice_or_idx.size)
    stride = int(slice_or_idx.stride)
    return slice(start, start + size * stride, stride)

