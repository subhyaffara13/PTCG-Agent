
def _log_io_metrics(
    direction: types.IoDirection,
    logical_bytes: int,
    start_time: float,
    parent_dir: epath.Path,
    initial_ts_metrics: Sequence[dict[str, Any]] | None = None,
):
  """Logs and records IO telemetry metrics for array serialization/deserialization."""
  duration = time.time() - start_time
  storage_type = path_utils.get_storage_type(parent_dir)

  _record_logical_metrics(
      direction,
      logical_bytes,
      duration,
      storage_type,
  )
  _record_raw_metrics(
      direction,
      logical_bytes,
      duration,
      storage_type,
      initial_ts_metrics=initial_ts_metrics,
  )

