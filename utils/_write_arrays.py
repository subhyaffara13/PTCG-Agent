
def _write_arrays(array_store_path: Any, arrs: list[Any],
                  arr_leaf_ids: list[int], ts_specs: list[Any | None],
                  distinct_locations: bool):
  paths = [array_store_path / str(leaf_id) for leaf_id in arr_leaf_ids]
  process_idx = None
  if not distinct_locations and jax.process_count() > 1:
    process_idx = jax.process_index()
  default_ts_specs = [ts_impl.get_tensorstore_spec(path, ocdbt=_USE_OCDBT,
                                                   process_idx=process_idx,
                                                   arr=arr)
                      for (path, arr) in zip(paths, arrs)]
  processed_ts_specs = [ts_impl.merge_nested_ts_specs(default_ts_spec, ts_spec)
                        for (default_ts_spec, ts_spec) in zip(default_ts_specs, ts_specs)]

  # sanity check the ts specs
  if len(ts_specs) > 0:  # verify the base path is shared for all arrays
    expected_path = processed_ts_specs[0]["kvstore"]["base"]["path"]  # shared base path
    for ts_spec, arr in zip(processed_ts_specs, arrs):
      assert ts_spec is not None
      ts_impl.verify_tensorstore_spec(ts_spec, arr, expected_path,
                                      ocdbt=_USE_OCDBT, check_metadata=True)

  async def _serialize_arrays():
    await asyncio.gather(*[
        ts_impl.async_serialize(arr, ts_spec, primary_host=None)
        for (arr, ts_spec) in zip(arrs, processed_ts_specs)])

  asyncio.run(_serialize_arrays())

