
def _get_cross_compile_backend(compile_only_backend):
  """Returns a real backend for cross-compilation via a real client.

  When cross-compiling via a compile-only client, checks if a real backend
  is available for the same platform. If so, returns it so compilation can
  leverage real hardware (e.g., for GPU kernel autotuning).
  """
  platform = compile_only_backend.platform
  try:
    real_backend = xb.get_backend(platform)
  except Exception:
    return None
  # Don't use the real backend if it's also a compile-only client.
  if isinstance(real_backend, _jax.CompileOnlyPyClient):
    return None
  # Don't use real backend if platform version is different, this can lead
  # to timeouts and hangs.
  if real_backend.platform_version != compile_only_backend.platform_version:
    return None
  return real_backend

