
def get_err_regex(message: str) -> str:
  """Constructs a regexp for the exception message.

  Args:
    message: an exception message.

  Returns:
    Regexp that ensures the message follows the standard chex formatting.
  """
  # (ERR_PREFIX + any symbols (incl. \n) + message)
  return f"{re.escape(ERR_PREFIX)}[\\s\\S]*{message}"

