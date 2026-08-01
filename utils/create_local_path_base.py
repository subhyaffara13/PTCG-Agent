
def create_local_path_base(testclass) -> epath.Path:
  return epath.Path(
      testclass.create_tempdir(name=_LOCAL_PATH_BASE_NAME).full_path
  )

