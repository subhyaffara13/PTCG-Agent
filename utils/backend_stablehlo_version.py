
def backend_stablehlo_version(platform=None) -> Sequence[int] | None:
  """Returns the StableHLO version of the backend.

  Returns None if the backend does not use PJRT C API or does not have
  stablehlo_current_version in the plugin attributes. This method can be used to
  skip features that are not available before certain stablehlo_current_version
  if the backend is a plugin and uses stablehlo_current_version.
  """
  backend = get_backend(platform)
  return getattr(backend, "stablehlo_current_version", None)

