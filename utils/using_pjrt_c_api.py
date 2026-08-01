
def using_pjrt_c_api(backend=None):
  return "PJRT C API" in get_backend(backend).platform_version

