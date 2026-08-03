from typing import Any

def _read_arrays(array_store_path: str | PathLike[str], arr_leaf_ids: list[int],
                 ts_specs: list[Any], shardings: list[Any]):
  # array_store_path = root / _LEAF_DATA_DIR / _ARRAY_STORE_DIRNAME
  arr_store_path = _norm_path(array_store_path)
  arr_paths = [arr_store_path / str(leaf_id) for leaf_id in arr_leaf_ids]

  # byte limiter to limit number of parallel reads, resizes to largest read
  byte_limiter = ts_impl._LimitInFlightBytes(10 * 1024 ** 3)  # 10 GB

  default_ts_specs = [ts_impl.get_tensorstore_spec(path, ocdbt=_USE_OCDBT,
                                                   process_idx=None)
                      for path in arr_paths]
  ts_specs = [ts_impl.merge_nested_ts_specs(default_ts_spec, ts_spec)
              for (default_ts_spec, ts_spec) in zip(default_ts_specs, ts_specs)]

  if len(ts_specs) > 0:  # verify the base path is shared for all arrays
    expected_path = ts_specs[0]["kvstore"]["base"]["path"]  # shared base path
    for ts_spec in ts_specs:
      ts_impl.verify_tensorstore_spec(ts_spec, arr=None, path=expected_path,
                                      ocdbt=_USE_OCDBT, check_metadata=False)

  async def _deserialize_arrays():
    return await asyncio.gather(*[
        ts_impl.async_deserialize(sharding, ts_spec, byte_limiter=byte_limiter)
        for (sharding, ts_spec) in zip(shardings, ts_specs)])

  return dict(zip(arr_leaf_ids, asyncio.run(_deserialize_arrays())))

