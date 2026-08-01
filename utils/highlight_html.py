
def highlight_html(code: str) -> str:
  """Add Python syntax highlighting to a Python code string.

  Usage:

  Example:

  ```python
  @dataclasses.dataclass
  class A:
    x: int

    def _repr_html_(self) -> str:
      from etils import ecolab  # Lazy-import ecolab

      return ecolab.highlight_html(repr(self))

  ```

  Args:
    code: The string to wrap

  Returns:
    The HTML string representation
  """
  theme = resource_utils.resource_import(
      'static/highlight.css', module='etils.ecolab'
  )
  # html
  html_str = """
  {theme}
  <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
  <pre><code class="language-python">{code}</code></pre>
  """
  html_str = epy.dedent(html_str)
  html_str = html_str.format(theme=theme, code=html.escape(code))
  return html_str

