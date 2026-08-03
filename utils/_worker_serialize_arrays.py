import time
from typing import Any, Dict

def _worker_serialize_arrays(
    arrays: Sequence[jax.Array],
    infos: Sequence[types.ParamInfo],
    args: Sequence[types.SaveArgs],
    replica_id: int,
    use_replica_parallel: bool,
    min_slice_bytes_for_replica_parallel: int | None,
    max_replicas_for_replica_parallel: int | None,
    primary_host: int | None,
    metadata_key: str | None,
    array_metadata_store: array_metadata_store_lib.Store | None,
    enable_replica_parallel_separate_folder: bool,
    ext_metadata: Dict[str, Any],
):
  """Worker function to serialize arrays."""
  try:
    initial_ts_metrics = ts.experimental_collect_matching_metrics(
        '/tensorstore/'
    )
  except Exception:  # pylint: disable=broad-except
    initial_ts_metrics = None
  total_start_time = time.time()
  rslices_per_array = _get_replica_slices(
      arrays,
      replica_id,
      use_replica_parallel,
      min_slice_bytes_for_replica_parallel,
      max_replicas_for_replica_parallel,
  )

  asyncio_utils.run_sync(
      _async_serialize_replica_slices(
          rslices_per_array,
          infos,
          args,
          primary_host=primary_host,
          metadata_key=metadata_key,
          array_metadata_store=array_metadata_store,
          enable_replica_parallel_separate_folder=enable_replica_parallel_separate_folder,
          use_replica_parallel=use_replica_parallel,
          ext_metadata=ext_metadata,
      )
  )
  if infos:
    total_io_bytes = sum(v.nbytes for v in rslices_per_array)
    _log_io_metrics(
        direction=types.IoDirection.WRITE,
        logical_bytes=total_io_bytes,
        start_time=total_start_time,
        parent_dir=infos[0].parent_dir,
        initial_ts_metrics=initial_ts_metrics,
    )

