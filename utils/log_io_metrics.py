import logging
import time

def log_io_metrics(
    size: int,
    start_time: float,
    gbytes_per_sec_metric: str,
    gbytes_metric: str | None = None,
    *,
    primary_host: int | None,
):
  """Logs the bytes per second metric."""
  time_elapsed = time.time() - start_time
  bytes_per_sec = (
      float('nan') if time_elapsed == 0 else float(size) / time_elapsed
  )
  logging.info(
      '[process=%d] %s: %s/s (total size: %s) (time elapsed: %s s) (global)',
      multihost.process_index(),
      gbytes_per_sec_metric,
      humanize.naturalsize(bytes_per_sec, binary=True, format='%.3f'),
      humanize.naturalsize(size, binary=True),
      time_elapsed,
  )
  if primary_host is None:
    logging.warning(
        'Global object size logging disabled for `primary_host=None`.'
    )
  elif multihost.is_primary_host(primary_host):
    jax.monitoring.record_scalar(
        gbytes_per_sec_metric, value=bytes_per_sec / (1024**3)
    )
    if gbytes_metric is not None:
      jax.monitoring.record_scalar(gbytes_metric, value=size / (1024**3))

