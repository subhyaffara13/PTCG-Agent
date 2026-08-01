
def _wgmma_accumulator_store_abstract_eval(acc, val):
  # Before discharge acc is a WGMMAAbstractAccumulatorRef. After discharge,
  # the discharge rule re-binds the primitive and acc becomes a ShapedArray.
  if isinstance(acc, gpu_core.WGMMAAbstractAccumulatorRef):
    inner = acc.inner_aval
    assert isinstance(inner, jax_core.ShapedArray)
  elif isinstance(acc, jax_core.ShapedArray):
    inner = acc
  else:
    raise TypeError(f"Expected WGMMAAbstractAccumulatorRef or ShapedArray, got {type(acc)}")
  if inner.shape != val.shape:
    raise ValueError(
        f"Accumulator shape {inner.shape} does not match value shape {val.shape}"
    )
  if inner.dtype != val.dtype:
    raise ValueError(
        f"Accumulator dtype {inner.dtype} does not match value dtype {val.dtype}"
    )
  effects: set[jax_core.Effect] = {gpu_core._wgmma_pipeline_effect}
  if isinstance(acc, gpu_core.WGMMAAbstractAccumulatorRef):
    effects.add(state.WriteEffect(0))
  return inner, effects

