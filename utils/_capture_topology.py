
def _capture_topology() -> tuple[int, int, int, str]:
  """Best-effort jax topology snapshot."""
  try:
    import jax  # pylint: disable=g-import-not-at-top

    devices = jax.devices()
    kind = devices[0].device_kind if devices else "unknown"
    return (
        jax.process_count(),
        jax.process_index(),
        jax.device_count(),
        kind,
    )
  except Exception:  # pylint: disable=broad-exception-caught
    return (1, 0, 0, "unknown")

