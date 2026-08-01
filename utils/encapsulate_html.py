
def encapsulate_html(html_src: str, compress: bool = True) -> str:
  """Encapsulates HTML source code into a duplication-safe container.

  Args:
    html_src: The HTML source code to encapsulate.
    compress: Whether to compress the HTML source code.

  Returns:
    An HTML output segment that can be displayed in a notebook environment or
    saved.
  """
  [converted] = encapsulate_streaming_html(
      [html_src], compress=compress, stealable=False
  )
  return converted.html_src

