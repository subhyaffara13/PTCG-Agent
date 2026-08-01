
def _glance_host(
    host_values: dict[str, float], keys: list[str] | None
) -> float | None:
  """Returns the first non-NaN value across candidate keys for one host."""
  for key in keys or []:
    if key in host_values and not math.isnan(host_values[key]):
      value = host_values[key]
      if "bytes" in key and "gb" not in key:
        return value / (1024**3)
      return value
  return None

