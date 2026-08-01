
def get_help_width() -> int:
  """Returns the integer width of help lines that is used in TextWrap."""
  size = shutil.get_terminal_size(fallback=(_DEFAULT_HELP_WIDTH, 1))
  return size.columns

