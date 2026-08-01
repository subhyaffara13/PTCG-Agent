
def _extract_int_from_repr(
    device: jax.Device,
    pattern: str,
) -> int | None:
  """Extracts an integer from the device repr using the given regex pattern."""
  match = re.search(pattern, repr(device))
  if match:
    if pattern not in _WARNED_REPR_PATTERNS:
      _WARNED_REPR_PATTERNS.add(pattern)
      logging.warning(
          'Pathways worker-key inference fell back to repr parsing for '
          'pattern=%r. Sample device=%r',
          pattern,
          device,
      )
    return int(match.group(1))
  return None

