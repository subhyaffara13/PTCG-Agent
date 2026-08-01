
def _summary_aggregates(
    per_host_matrix: np.ndarray, keys: list[str]
) -> BenchmarkSummary:
  """Computes per-metric max/min/mean (p50/p99 with >1 host) across hosts.

  NaN entries (a host that didn't report a key) are dropped per column, so
  primary-only events still aggregate from the hosts that did report. "max" is
  the MLPerf-honest headline (slowest rank for time, smallest for throughput —
  callers translate per metric).

  Args:
    per_host_matrix: (host_count, metric_count) values; NaN where unreported.
    keys: Metric keys, one per matrix column.

  Returns:
    Metric key -> {stat: value}; empty if the matrix or keys are empty.
  """
  if per_host_matrix.size == 0 or len(keys) == 0:
    return {}
  out: dict[str, dict[str, float]] = {}
  for j, key in enumerate(keys):
    column = per_host_matrix[:, j]
    column = column[~np.isnan(column)]
    if column.size == 0:
      continue
    entry = {
        "max": float(np.max(column)),
        "min": float(np.min(column)),
        "mean": float(np.mean(column)),
    }
    if column.size > 1:
      entry["p50"] = float(np.percentile(column, 50))
      entry["p99"] = float(np.percentile(column, 99))
    out[key] = entry
  return out

