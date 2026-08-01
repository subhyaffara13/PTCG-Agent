
def _get_backend_uncached(
    platform: None | str | xla_client.Client = None
) -> xla_client.Client:
  # TODO(mattjj,skyewm): remove this input polymorphism after we clean up how
  # 'backend' values are handled
  if platform is not None and not isinstance(platform, str):
    return platform

  platform = (platform or _XLA_BACKEND.value or _PLATFORM_NAME.value or None)

  bs = backends()
  if platform is not None:
    platform = canonicalize_platform(platform)
    backend = bs.get(platform, None)
    if backend is None:
      if platform in _backend_errors:
        raise RuntimeError(f"Backend '{platform}' failed to initialize: "
                           f"{_backend_errors[platform]}. "
                           f'Available backends are {list(bs)}')
      raise RuntimeError(
          f"Unknown backend {platform}. Available backends are {list(bs)}")
    return backend
  else:
    assert _default_backend is not None
    return _default_backend

