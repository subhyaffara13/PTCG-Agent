
def _record_raw_metrics(
    direction: types.IoDirection,
    logical_bytes: int,
    duration: float,
    storage_type: str,
    initial_ts_metrics: Sequence[dict[str, Any]] | None = None,
):
  """Records raw metrics collected from TensorStore."""
  if initial_ts_metrics is None:
    return

  try:
    final_ts_metrics = ts.experimental_collect_matching_metrics('/tensorstore/')
  except Exception:  # pylint: disable=broad-except
    final_ts_metrics = None

  if final_ts_metrics is None:
    return

  initial_bytes = ts_utils.get_total_bytes_from_tensorstore(
      initial_ts_metrics, direction
  )
  final_bytes = ts_utils.get_total_bytes_from_tensorstore(
      final_ts_metrics, direction
  )
  raw_bytes = final_bytes - initial_bytes

  if raw_bytes <= 0:
    return

  raw_throughput = raw_bytes / duration if duration > 0 else 0
  logging.info(
      '[process=%d] Raw %s throughput: %s/s (total gbytes: %s) (time elapsed:'
      ' %s s) (per-host)',
      multihost.process_index(),
      f'/jax/orbax/{direction.value}/worker/io/raw',
      humanize.naturalsize(raw_throughput, binary=True, format='%.3f'),
      humanize.naturalsize(raw_bytes, binary=True),
      duration,
  )
  jax.monitoring.record_scalar(
      f'/jax/orbax/{direction.value}/worker/io/raw/gbytes',
      raw_bytes / (1024**3),
      storage_type=storage_type,
  )
  jax.monitoring.record_scalar(
      f'/jax/orbax/{direction.value}/worker/io/raw/throughput/gbytes_per_sec',
      raw_throughput / (1024**3),
      storage_type=storage_type,
  )

  if logical_bytes > 0:
    ratio = float(raw_bytes) / logical_bytes
    logging.info(
        '[process=%d] %s ratio (raw/logical): %.3f (%s / %s)',
        multihost.process_index(),
        direction.value.capitalize(),
        ratio,
        humanize.naturalsize(raw_bytes, binary=True),
        humanize.naturalsize(logical_bytes, binary=True),
    )
    jax.monitoring.record_scalar(
        f'/jax/orbax/{direction.value}/worker/io/compression_ratio',
        ratio,
        storage_type=storage_type,
    )
    if direction == types.IoDirection.WRITE:
      jax.monitoring.record_scalar(
          '/jax/orbax/write/worker/io/compressed_gbytes',
          raw_bytes / (1024**3),
          storage_type=storage_type,
      )

