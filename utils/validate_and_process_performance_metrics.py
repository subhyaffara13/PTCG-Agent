from typing import Any

def validate_and_process_performance_metrics(
    performance_metrics: Any,
) -> dict[str, float]:
  """Validates and processes performance_metrics field."""
  if performance_metrics is None:
    return {}

  _validate_type(performance_metrics, [dict, StepStatistics])
  if isinstance(performance_metrics, StepStatistics):
    performance_metrics = dataclasses.asdict(performance_metrics)

  for k in performance_metrics:
    _validate_type(k, str)

  return {
      metric: val
      for metric, val in performance_metrics.items()
      if isinstance(val, float)
  }

