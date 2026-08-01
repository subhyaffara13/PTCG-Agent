
def CEscape(text, as_utf8) -> str:
  """Escape a bytes string for use in an text protocol buffer.

  Args:
    text: A byte string to be escaped.
    as_utf8: Specifies if result may contain non-ASCII characters.
        In Python 3 this allows unescaped non-ASCII Unicode characters.
        In Python 2 the return value will be valid UTF-8 rather than only ASCII.
  Returns:
    Escaped string (str).
  """
  # Python's text.encode() 'string_escape' or 'unicode_escape' codecs do not
  # satisfy our needs; they encodes unprintable characters using two-digit hex
  # escapes whereas our C++ unescaping function allows hex escapes to be any
  # length.  So, "\0011".encode('string_escape') ends up being "\\x011", which
  # will be decoded in C++ as a single-character string with char code 0x11.
  text_is_unicode = isinstance(text, str)
  if as_utf8:
    if text_is_unicode:
      return text.translate(_str_escapes)
    else:
      return _DecodeUtf8EscapeErrors(text)
  else:
    if text_is_unicode:
      text = text.encode('utf-8')
    return ''.join([_byte_escapes[c] for c in text])

