
def tag(name: str, **attributes: str | list[str] | None) -> Callable[..., str]:
  """Create a html tag.

  Usage:

  ```python
  tag('div', id='x')('content') == '<div id="x">content</div>'
  ```

  Args:
    name: Tag name
    **attributes: Attributes of the tag

  Returns:
    The HTML string
  """
  # Could be much more optimized by first building the graph of nested
  # element, then joining individual parts

  attributes = _format_tag_attributes(attributes)

  def apply(*content: str) -> str:
    content = ''.join(content)
    return f'<{name}{attributes}>{content}</{name}>'

  return apply

