
def dilate_dim(d: DimSize, dilation: DimSize) -> DimSize:
  """max(0, 1 + dilation * (d - 1)).

  Assumes dilation >= 1.
  """
  if definitely_equal(dilation, 1):  # fast path
    return d
  return max_dim(1 + dilation * (d - 1), 0)

