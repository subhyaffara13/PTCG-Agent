import math


def _glance_agg(
    aggregates: dict[str, dict[str, float]],
    keys: list[str],
    stat: str = "mean",
) -> float | None:
  """Returns the first non-NaN `stat` across candidate keys, or None."""
  for key in keys:
    stats = aggregates.get(key)
    if stats is not None:
      value = stats.get(stat)
      if value is not None and not math.isnan(value):
        if "bytes" in key and "gb" not in key:
          return value / (1024**3)
        return value
  return None

