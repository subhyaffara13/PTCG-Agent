
def is_cache_used(backend: xla_client.Client) -> bool:
  """Check if cache is used and report adoption metrics one-time per task.
  The cache may be initialized during the first call to this function.
  """
  # Return _cache_used directly if _cache_checked is True. If _cache_checked is
  # False, set it to True, report metrics and return if cache is used. This
  # provides a mechanism to report the metrics once per task. Note that
  # reset_cache() will reset _cache_checked and _cache_used also.
  global _cache_checked, _cache_used
  with _cache_initialized_mutex:
    if _cache_checked:
      return _cache_used

  with _cache_initialized_mutex:
    if not _cache_checked:
      _cache_checked = True

      # Persistent compilation cache only implemented on TPU and GPU and the
      # backend that supports serialization of executables.
      # TODO(skye): add warning when initializing cache on unsupported default
      # platform
      supported_platforms = ["tpu", "gpu", "cpu", "neuron"]

      if not _is_cache_enabled():
        monitoring.record_event('/jax/compilation_cache/task_disabled_cache')
      elif (
          backend.platform in supported_platforms
          and getattr(backend, "supports_executable_serialization", True)
      ):
        monitoring.record_event('/jax/compilation_cache/tasks_using_cache')
        _cache_used = True
      return _cache_used

  return False

