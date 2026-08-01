
def estimate_read_memory_footprint(
    t: ts.TensorStore, domain: ts.IndexDomain
) -> int:
  """Estimates memory required to read a given domain."""
  rank = t.rank
  num_bytes = t.dtype.numpy_dtype.itemsize
  chunk_template = t.chunk_layout.read_chunk_template
  if domain is None:
    domain = t.domain
  origin = domain.origin
  shape = domain.shape
  chunk_origin = chunk_template.origin
  chunk_shape = chunk_template.shape

  # Some TensorStore drivers are not chunked, e.g. the inline 'array' driver.
  # For those, instead of returning a near-infinite memory footprint, estimate
  # the footprint as the entire shape.
  for i in range(rank):
    if not chunk_template[i].finite:
      return domain.size * num_bytes

  # Otherwise, if we have a chunked driver, estimate based on chunk size.
  for i in range(rank):
    origin_value = origin[i]
    chunk_origin_value = chunk_origin[i]
    chunk_size = chunk_shape[i]
    lower = origin_value - chunk_origin_value
    upper = origin_value + shape[i] - chunk_origin_value
    lower_aligned = lower // chunk_size * chunk_size
    upper_aligned = -(-upper // chunk_size) * chunk_size
    num_bytes *= upper_aligned - lower_aligned

  return num_bytes


def estimate_read_memory_footprint(t: ts.TensorStore,
                                   domain: ts.IndexDomain) -> int:
  rank = t.rank
  num_bytes = t.dtype.numpy_dtype.itemsize
  chunk_template = t.chunk_layout.read_chunk_template
  if domain is None:
    domain = t.domain
  origin = domain.origin
  shape = domain.shape
  chunk_origin = chunk_template.origin
  chunk_shape = chunk_template.shape

  # Some TensorStore drivers are not chunked, e.g. the inline 'array' driver.
  # For those, instead of returning a near-infinite memory footprint, estimate
  # the footprint as the entire shape.
  for i in range(rank):
    if not chunk_template[i].finite:
      return domain.size * num_bytes

  # Otherwise, if we have a chunked driver, estimate based on chunk size.
  for i in range(rank):
    origin_value = origin[i]
    chunk_origin_value = chunk_origin[i]
    chunk_size = chunk_shape[i]
    lower = origin_value - chunk_origin_value
    upper = origin_value + shape[i] - chunk_origin_value
    lower_aligned = lower // chunk_size * chunk_size
    upper_aligned = -(-upper // chunk_size) * chunk_size
    num_bytes *= (upper_aligned - lower_aligned)

  return num_bytes

