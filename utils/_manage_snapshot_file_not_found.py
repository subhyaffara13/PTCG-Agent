
def _manage_snapshot_file_not_found(
    ignore_errors: bool, formatted_message: str
) -> Iterator[None]:
  """Context manager to optionally suppress FileNotFoundError."""
  try:
    yield
  except FileNotFoundError:
    if ignore_errors:
      logging.warning(formatted_message, exc_info=True)
    else:
      raise

