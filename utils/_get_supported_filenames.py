
def _get_supported_filenames(filename: str | None = None) -> list[str]:
  filename = filename or _DATA_FILENAME
  return [filename, _DATA_FILENAME, 'metadata']

