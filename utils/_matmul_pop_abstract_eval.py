
def _matmul_pop_abstract_eval(*, shape, dtype, **_):
  if dtype not in map(jnp.dtype, [jnp.float32, jnp.int32]):
    raise ValueError(
        f"Only float32 and int32 accumulators are supported, got {dtype}"
    )
  return jax_core.ShapedArray(shape, dtype), {mxu_effect}

