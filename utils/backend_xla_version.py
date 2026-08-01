
def backend_xla_version(platform=None) -> int | None:
  """Returns the XLA version of the backend.

  Returns None if the backend does not use PJRT C API or does not have
  xla_version in the plugin attributes. This method can be used to skip features
  that are not available before certain xla_version if the backend is a
  plugin and uses xla_version.
  """
  backend = get_backend(platform)
  return getattr(backend, "xla_version", None)

