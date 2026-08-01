
def siblings(*args: RenderableTreePart | str) -> RenderableTreePart:
  """Builds a Siblings part from inline arguments.

  Args:
    *args: Sequence of renderables or strings (which will be wrapped in Text).

  Returns:
    A new Siblings part containing these concatenated together.
  """
  parts = []
  for arg in args:
    if isinstance(arg, str):
      parts.append(Text(arg))
    elif isinstance(arg, Siblings):
      parts.extend(arg.children)
    elif isinstance(arg, EmptyPart):
      pass
    elif isinstance(arg, RenderableTreePart):
      parts.append(arg)
    else:
      raise ValueError(f"Invalid argument type {type(arg)}")
  return Siblings(tuple(parts))

