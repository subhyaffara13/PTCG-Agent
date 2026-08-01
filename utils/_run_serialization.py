
def _run_serialization(arrays, tensorstore_specs):
  """Legacy serialization of a list of arrays."""
  async def _run_serializer():
    future_writer = jax.tree_util.tree_map(async_serialize, arrays, tensorstore_specs)
    return await asyncio.gather(*future_writer)
  asyncio.run(_run_serializer())

