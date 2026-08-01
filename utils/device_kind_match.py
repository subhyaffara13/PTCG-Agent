
def device_kind_match(device_patterns: str | Sequence[str]) -> str | None:
  device_kind = xla_bridge.devices()[0].device_kind
  matching_pattern = pattern_search(device_patterns, device_kind)
  return matching_pattern

