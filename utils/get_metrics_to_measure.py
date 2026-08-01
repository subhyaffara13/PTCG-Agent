
def get_metrics_to_measure(options: BenchmarkOptions) -> list[str]:
  """Returns the list of metrics to measure.

  Cheap captures (time, rss, jax_monitoring, device_memory, tensorstore)
  are always on. Tracemalloc is opt-in because its per-allocation
  snapshots have measurable runtime overhead.

  Args:
    options: Benchmark options; tracemalloc is added when
      metric_tracemalloc_enabled is set.

  Returns:
    The metric names to capture for each measured operation.
  """
  metrics = metric_lib.default_metrics()
  if options.metric_tracemalloc_enabled:
    metrics.append("tracemalloc")
  return metrics

