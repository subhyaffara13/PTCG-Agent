
def pjrt_c_api_version_at_least(major_version: int, minor_version: int) -> bool:
  pjrt_c_api_versions = xla_bridge.backend_pjrt_c_api_version()
  if pjrt_c_api_versions is None:
    return True
  return pjrt_c_api_versions >= (major_version, minor_version)

