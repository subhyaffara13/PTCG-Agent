
def base64_utf8_stringify(bs: bytes) -> str:
  """Converts bytes to a base64-encoded utf-8 string.

  Args:
    bs: The bytes to convert.

  Returns:
    The base64-encoded utf-8 string.
  """
  return base64.b64encode(bs).decode("utf-8")

