
def trim_docstring(docstring: str) -> str:
  """Removes indentation from triple-quoted strings.

  This is the function specified in PEP 257 to handle docstrings:
  https://www.python.org/dev/peps/pep-0257/.

  Args:
    docstring: str, a python docstring.

  Returns:
    str, docstring with indentation removed.
  """
  if not docstring:
    return ''

  # If you've got a line longer than this you have other problems...
  max_indent = 1 << 29

  # Convert tabs to spaces (following the normal Python rules)
  # and split into a list of lines:
  lines = docstring.expandtabs().splitlines()

  # Determine minimum indentation (first line doesn't count):
  indent = max_indent
  for line in lines[1:]:
    stripped = line.lstrip()
    if stripped:
      indent = min(indent, len(line) - len(stripped))
  # Remove indentation (first line is special):
  trimmed = [lines[0].strip()]
  if indent < max_indent:
    for line in lines[1:]:
      trimmed.append(line[indent:].rstrip())
  # Strip off trailing and leading blank lines:
  while trimmed and not trimmed[-1]:
    trimmed.pop()
  while trimmed and not trimmed[0]:
    trimmed.pop(0)
  # Return a single string:
  return '\n'.join(trimmed)

