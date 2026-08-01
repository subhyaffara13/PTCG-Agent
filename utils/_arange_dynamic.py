
def _arange_dynamic(
    start: DimSize, stop: DimSize, step: DimSize, dtype: DTypeLike) -> Array:
  # Here if at least one of start, stop, step are dynamic.
  if any(not core.is_dim(v) for v in (start, stop, step)):
    raise ValueError(
        "In arange with non-constant arguments all of start, stop, and step "
        f"must be either dimension expressions or integers: start={start}, "
        f"stop={stop}, step={step}")
  # Must resolve statically if step is {<0, ==0, >0}
  try:
    if step == 0:
      raise ValueError("arange has step == 0")
    step_gt_0 = (step > 0)
  except core.InconclusiveDimensionOperation as e:
    raise core.InconclusiveDimensionOperation(
        f"In arange with non-constant arguments the step ({step}) must " +
        f"be resolved statically if it is > 0 or < 0.\nDetails: {e}")
  gap = step if step_gt_0 else - step
  distance = (stop - start) if step_gt_0 else (start - stop)
  size = core.max_dim(0, distance + gap - 1) // gap
  return (array(start, dtype=dtype) +
          array(step, dtype=dtype) * lax.iota(dtype, size))

