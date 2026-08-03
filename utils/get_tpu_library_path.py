import os

def get_tpu_library_path() -> str | None:
  path_from_env = os.getenv('TPU_LIBRARY_PATH')
  if path_from_env is not None:
    if os.path.isfile(path_from_env):
      return path_from_env
    warning_message = (
        f'TPU_LIBRARY_PATH is set to a non-existent path: {path_from_env}.'
        ' Falling back to default libtpu path. Please unset TPU_LIBRARY_PATH'
        ' or set it to a valid path.'
    )
    warnings.warn(warning_message)

  libtpu_module = maybe_import_libtpu()
  if libtpu_module is not None:
    return libtpu_module.get_library_path()

  return None

