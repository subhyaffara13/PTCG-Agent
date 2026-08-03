from typing import Any, Callable

def _fn_children(fn: Callable[..., Any]) -> list[Node]:
  """Build the fn children."""
  children = []
  # Add docstring
  try:
    doc = fn.__doc__
  except Exception:  # pylint: disable=broad-except
    pass
  else:
    if doc:
      children.append(HtmlNode(_obj_html_repr(doc)))

  # Add signature
  try:
    sig = inspect.Signature.from_callable(fn)
  except Exception:  # pylint: disable=broad-except
    # Many builtins do not expose any signature information
    pass
  else:
    for param in sig.parameters.values():
      name = param.name
      if param.kind == inspect.Parameter.VAR_POSITIONAL:
        name = f'*{name}'
      elif param.kind == inspect.Parameter.VAR_KEYWORD:
        name = f'**{name}'
      name = H.span(class_=['preview'])(name)

      if param.annotation is inspect.Parameter.empty:
        annotations = ''
      else:
        annotations = f': {_obj_html_repr(param.annotation)}'
      if param.default is inspect.Parameter.empty:
        default = ''
      else:
        default = f' = {_obj_html_repr(param.default)}'
      node = HtmlNode(name + annotations + default)
      children.append(node)
  return children

