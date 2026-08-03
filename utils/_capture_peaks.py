import logging

def _capture_peaks() -> list[int] | None:
  """Returns the per-local-device peak_bytes_in_use, or None if unsupported."""
  peaks: list[int] = []
  for d in jax.local_devices():
    try:
      stats = d.memory_stats()
      if not stats or "peak_bytes_in_use" not in stats:
        logging.warning(
            "Device %s does not support 'peak_bytes_in_use' in memory_stats.", d
        )
        return None  # Invalidate measurement if any device lacks the stat
      peaks.append(int(stats["peak_bytes_in_use"]))
    except jax.errors.JaxRuntimeError as e:
      if "MemoryStats is only supported for addressable PjRt devices" in str(e):
        logging.warning(
            "Cannot get memory stats for device %s, it may not be an"
            " addressable PjRt device: %s",
            d,
            e,
        )
        return None  # Invalidate measurement if any device is not supported
      else:
        logging.exception(
            "Unexpected JAX error with memory_stats on device %s: %s", d, e
        )
        raise  # Re-raise other unexpected JaxRuntimeErrors
    except (AttributeError, TypeError):
      logging.warning(
          "memory_stats() not available or in unexpected format for device %s.",
          d,
      )
      return None
  return peaks

