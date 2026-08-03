import pathlib

def is_gcs_path(path: pathlib.PurePosixPath) -> bool:
  return path.as_posix().startswith(_GCS_PATH_PREFIX)

