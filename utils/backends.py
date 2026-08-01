
def backends() -> dict[str, xla_client.Client]:
  global _backends
  global _backend_errors
  global _default_backend
  global _at_fork_handler_installed

  _discover_and_register_pjrt_plugins()

  with _backend_lock:
    if _backends:
      return _backends

    # os.register_at_fork only exists on Unix.
    if not _at_fork_handler_installed and hasattr(os, "register_at_fork"):
      os.register_at_fork(before=_at_fork)
      _at_fork_handler_installed = True

    if jax_platforms := config.jax_platforms.value:
      platforms = []
      # Allow platform aliases in the list of platforms.
      for platform in jax_platforms.split(","):
        platforms.extend(expand_platform_alias(platform))
      priorities = range(len(platforms), 0, -1)
      # If the user specified a list of platforms explicitly, always fail
      # loudly.
      fail_quietly_list = [False] * len(platforms)
      platform_registrations = list(
        zip(platforms, priorities, fail_quietly_list))
    else:
      platform_registrations = [
          (platform, registration.priority, registration.fail_quietly)
          for platform, registration
          in _backend_factories.items()
      ]
    default_priority = -1000
    for platform, priority, fail_quietly in platform_registrations:
      try:
        if platform == "cuda" and not hardware_utils.has_visible_nvidia_gpu():
          continue

        backend = _init_backend(platform)
        _backends[platform] = backend

        if priority > default_priority:
          _default_backend = backend
          default_priority = priority
      except Exception as err:
        err_msg = f"Unable to initialize backend '{platform}': {err}"
        if fail_quietly:
          _backend_errors[platform] = str(err)
          logger.info(err_msg)
        else:
          if config.jax_platforms.value:
            err_msg += " (set JAX_PLATFORMS='' to automatically choose an available backend)"
          else:
            err_msg += " (you may need to uninstall the failing plugin package, or set JAX_PLATFORMS=cpu to skip this backend.)"
          raise RuntimeError(err_msg)

    assert _default_backend is not None
    if not config.jax_platforms.value:
      _suggest_missing_backends()
    return _backends

