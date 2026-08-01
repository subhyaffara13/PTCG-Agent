
def MessageToBytes(message, **kwargs) -> bytes:
  """Convert protobuf message to encoded text format.  See MessageToString."""
  text = MessageToString(message, **kwargs)
  if isinstance(text, bytes):
    return text
  codec = 'utf-8' if kwargs.get('as_utf8') else 'ascii'
  return text.encode(codec)

