
def _wgmma_accumulator_deref_abstract_eval(acc, **_):
  # Dereferencing implies flushing so we have a wgmma pipeline effect.
  ret = acc.inner_aval if isinstance(acc, state.AbstractRef) else acc
  assert isinstance(ret, jax_core.ShapedArray), acc
  return ret, {gpu_core._wgmma_pipeline_effect}

