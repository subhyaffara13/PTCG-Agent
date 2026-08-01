
def diff_str(a: str | object, b: str | object) -> str:
  """Pretty diff between 2 objects.

  Args:
    a: Object/str to compare
    b: Object/str to compare

  Returns:
    The diff string
  """
  if not isinstance(a, str):
    a = pretty_repr(a).split('\n')
  if not isinstance(b, str):
    b = pretty_repr(b).split('\n')

  diff = difflib.ndiff(a, b)
  return '\n'.join(diff)

