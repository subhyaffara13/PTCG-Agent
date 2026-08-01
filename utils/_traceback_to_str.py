
def _traceback_to_str(traceback: TracebackType) -> str:
  """Convert a traceback to a string for export."""
  return "".join(tb_lib.format_list(tb_lib.extract_tb(traceback))).rstrip("\n")

