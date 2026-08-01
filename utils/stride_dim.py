
def stride_dim(d: DimSize, window_size: DimSize, window_stride: DimSize) -> DimSize:
  """max(0, (d - window_size) // window_stride + 1)

  If d < window_size, returns 0.
  We assume window_size >= 1 and window_stride >= 1.
  """
  # If d < window_size then (d - window_size) // window_stride < 0
  return max_dim((d - window_size) // window_stride + 1, 0)

