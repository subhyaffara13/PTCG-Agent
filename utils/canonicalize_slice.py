
def canonicalize_slice(
    s: slice,
    axis_size: DimSize
  ) -> tuple[DimSize, DimSize, DimSize]:
  """Computes the start index, step, and size of the slice `x[s]`.

  This is similar to `s.indices(axis_size)`, except that it returns
  `(start, step, size)`, and it works when the slice and/or the
  `axis_size` are symbolic.

  See https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding
  """
  def convert_to_index(d: DimSize) -> DimSize:
    # Convert np.array and jax.Array to int, leave symbolic dimensions alone
    try:
      return operator.index(d)
    except:
      return d

  # Must resolve statically if step is {<0, ==0, >0}
  step = convert_to_index(s.step) if s.step is not None else 1
  try:
    if step == 0:
      raise ValueError("slice step cannot be zero")
    step_gt_0 = (step > 0)
  except InconclusiveDimensionOperation as e:
    raise InconclusiveDimensionOperation(
        f"In slice with non-constant elements the step ({step}) must " +
        f"be resolved statically if it is > 0 or < 0.\nDetails: {e}")

  def clamp_index(i: DimSize, which: str):
    try:
      i_ge_0 = (i >= 0)
    except InconclusiveDimensionOperation as e:
      raise InconclusiveDimensionOperation(
          f"In slice with non-constant elements the {which} ({i}) must " +
          f"be resolved statically if it is >= 0.\nDetails: {e}")
    if i_ge_0:
      if step_gt_0:
        return min_dim(axis_size, i)
      else:
        return min_dim(axis_size - 1, i)
    else:
      if step_gt_0:
        return max_dim(0, axis_size + i)
      else:
        return max_dim(-1, axis_size + i)

  if s.start is None:
    start = 0 if step_gt_0 else axis_size - 1
  else:
    start = clamp_index(convert_to_index(s.start), "start")

  if s.stop is None:
    stop = axis_size if step_gt_0 else -1
  else:
    stop = clamp_index(convert_to_index(s.stop), "stop")

  gap = step if step_gt_0 else - step
  distance = (stop - start) if step_gt_0 else (start - stop)
  slice_size = max_dim(0, distance + gap - 1) // gap
  return start, step, slice_size

