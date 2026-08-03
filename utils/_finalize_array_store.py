import os

def _finalize_array_store(kvstore_path, distinct_locations: bool):
  """When multiple processes are writing, they must write to a per-process
  location followed by combining them via no-copy links to the final location.
  """
  # only in multiprocess case and only process 0
  if distinct_locations or jax.process_count() == 1 or jax.process_index() != 0:
    return
  dummy_key_path = os.path.join(kvstore_path, "dummy_key")
  combined_kvstore = ts_impl.get_tensorstore_spec(
      dummy_key_path, ocdbt=True, process_idx=None)["kvstore"]
  children_kvstores = [ts_impl.get_tensorstore_spec(
      dummy_key_path, ocdbt=True, process_idx=i)["kvstore"]
      for i in range(jax.process_count())]
  _ = combined_kvstore.pop("path")
  _ = [kvstore.pop("path") for kvstore in children_kvstores]
  asyncio.run(ts_impl.combine_kvstores(combined_kvstore, children_kvstores))

