
def string_to_base64(text: str) -> str:
  """Encodes a string to base64 format.

  Args:
    text: The string to encode.

  Returns:
    The base64-encoded string.
  """
  return base64_utf8_stringify(text.encode("utf-8"))

