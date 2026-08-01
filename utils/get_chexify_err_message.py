
def get_chexify_err_message(name: str, msg: str = "") -> str:
  """Constructs an error message for the chexify exception."""
  return f"{ERR_PREFIX}chexify assertion '{name}' failed: {msg}"

