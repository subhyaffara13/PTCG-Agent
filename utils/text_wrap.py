
def text_wrap(
    text: str,
    length: int | None = None,
    indent: str = '',
    firstline_indent: str | None = None,
) -> str:
  """Wraps a given text to a maximum line length and returns it.

  It turns lines that only contain whitespace into empty lines, keeps new lines,
  and expands tabs using 4 spaces.

  Args:
    text: Text to wrap.
    length: Maximum length of a line, includes indentation. If this is `None`
      then use `get_help_width()`.
    indent: Indent for all but first line.
    firstline_indent: Indent for first line. If `None`, fall back to `indent`.

  Returns:
    The wrapped text.

  Raises:
    ValueError: Raised if indent or firstline_indent not shorter than length.
  """
  # Get defaults where callee used None
  if length is None:
    length = get_help_width()
  if indent is None:
    indent = ''
  if firstline_indent is None:
    firstline_indent = indent

  if len(indent) >= length:
    raise ValueError('Length of indent exceeds length')
  if len(firstline_indent) >= length:
    raise ValueError('Length of first line indent exceeds length')

  text = text.expandtabs(4)

  result = []
  # Create one wrapper for the first paragraph and one for subsequent
  # paragraphs that does not have the initial wrapping.
  wrapper = textwrap.TextWrapper(
      width=length, initial_indent=firstline_indent, subsequent_indent=indent)
  subsequent_wrapper = textwrap.TextWrapper(
      width=length, initial_indent=indent, subsequent_indent=indent)

  # textwrap does not have any special treatment for newlines. From the docs:
  # "...newlines may appear in the middle of a line and cause strange output.
  # For this reason, text should be split into paragraphs (using
  # str.splitlines() or similar) which are wrapped separately."
  for paragraph in (p.strip() for p in text.splitlines()):
    if paragraph:
      result.extend(wrapper.wrap(paragraph))
    else:
      result.append('')  # Keep empty lines.
    # Replace initial wrapper with wrapper for subsequent paragraphs.
    wrapper = subsequent_wrapper

  return '\n'.join(result)

