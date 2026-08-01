
def _has_tensorstore_data_files(path: epath.Path) -> bool:
  return is_ocdbt_checkpoint(path) or any(_has_zarray_files(path))

