
def validate_and_process_metrics(
    metrics: Any, additional_metrics: Optional[Any] = None
) -> dict[str, Any]:
  """Validates and processes metrics field."""
  metrics = metrics or {}

  _validate_type(metrics, dict)
  for k in metrics:
    _validate_type(k, str)
  validated_metrics = metrics.copy()

  if additional_metrics is not None:
    _validate_type(additional_metrics, dict)
    for k, v in additional_metrics.items():
      _validate_type(k, str)
      validated_metrics[k] = v

  return validated_metrics

