from typing import Any

def _run_deserialization(shardings: Sequence[jax.sharding.Sharding | Format],
                        tensorstore_specs: Sequence[dict[str, Any] | ts.Spec],
                        global_shapes: Sequence[array.Shape] | None = None,
                        dtypes: Sequence[typing.DTypeLike] | None = None,
                        concurrent_gb: int = 32):
  """Legacy deserialization of a list of arrays. Optionally pass global_shapes
  and dtypes for type-checking.
  """
  concurrent_bytes = concurrent_gb * 10**9

  async def _run_deserializer():
    # Object should be created once per process.
    byte_limiter = _LimitInFlightBytes(concurrent_bytes)

    future_arrays = jax.tree_util.tree_map(
        partial(async_deserialize, byte_limiter=byte_limiter),
        list(shardings), list(tensorstore_specs),
        [None] * len(tensorstore_specs) if global_shapes is None else global_shapes,
        [None] * len(tensorstore_specs) if dtypes is None else dtypes)
    return await asyncio.gather(*future_arrays)
  return asyncio.run(_run_deserializer())

