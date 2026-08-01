
def erase_and_create_empty(directory: epath.PathLike) -> epath.Path:
  """Creates an empty directory, erasing existing if present.

  Generally should be avoided in production code, as the heedless deletion is
  not very safe.

  Args:
    directory: directory to create.

  Returns:
    The created directory.
  """
  directory = epath.Path(directory)
  if directory.exists():
    directory.rmtree()
  directory.mkdir()
  return directory

