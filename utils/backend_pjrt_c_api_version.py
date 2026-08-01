
def backend_pjrt_c_api_version(platform=None) -> tuple[int, int] | None:
  """Returns the PJRT C API version of the backend.

  Returns None if the backend does not use PJRT C API.
  """
  backend = get_backend(platform)
  if hasattr(backend, "pjrt_c_api_major_version") and hasattr(
      backend, "pjrt_c_api_minor_version"
  ):
    return (backend.pjrt_c_api_major_version, backend.pjrt_c_api_minor_version)
  return None

