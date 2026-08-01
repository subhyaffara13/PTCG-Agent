
def _record_logical_metrics(
    direction: types.IoDirection,
    logical_bytes: int,
    duration: float,
    storage_type: str,
):
  """Records logical bytes, throughput, and duration to JAX monitoring."""
  logical_throughput = logical_bytes / duration if duration > 0 else 0

  logging.info(
      '[process=%d] %s throughput: %s/s (total gbytes: %s) (time elapsed: %s s)'
      ' (per-host)',
      multihost.process_index(),
      f'/jax/orbax/{direction.value}/worker/io/requested',
      humanize.naturalsize(logical_throughput, binary=True, format='%.3f'),
      humanize.naturalsize(logical_bytes, binary=True),
      duration,
  )

  jax.monitoring.record_event_duration_secs(
      f'/jax/orbax/{direction.value}/worker/total_duration_secs',
      duration,
      storage_type=storage_type,
  )

  jax.monitoring.record_scalar(
      f'/jax/orbax/{direction.value}/worker/io/requested/gbytes',
      logical_bytes / (1024**3),
      storage_type=storage_type,
  )
  jax.monitoring.record_scalar(
      f'/jax/orbax/{direction.value}/worker/io/requested/throughput/gbytes_per_sec',
      logical_throughput / (1024**3),
      storage_type=storage_type,
  )

