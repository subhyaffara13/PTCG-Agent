
def _slice_per_host(
    per_host_values: list[tuple[int, dict[str, float]]], name: str
) -> list[tuple[int, dict[str, float]]]:
  """Per-host values for one capture name, with the `{name}::` prefix stripped."""
  return [(idx, _slice_namespace(vals, name)) for idx, vals in per_host_values]

