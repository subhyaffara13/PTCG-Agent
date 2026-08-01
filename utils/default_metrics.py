
def default_metrics() -> list[str]:
  """Returns the default metrics to measure."""
  return [
      "time",
      "rss",
      "jax_monitoring",
      "device_memory",
      "tensorstore",
  ]

