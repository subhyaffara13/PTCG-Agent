
def _open(
    filepath: str, mode: str, _open_func: abc.Callable[..., IO[AnyStr]] = open
) -> IO[AnyStr]:
  """Opens a file.

  Like open(), but ensure that we can open real files even if tests stub out
  open().

  Args:
    filepath: A filepath.
    mode: A mode.
    _open_func: A built-in open() function.

  Returns:
    The opened file object.
  """
  return _open_func(filepath, mode, encoding='utf-8')

