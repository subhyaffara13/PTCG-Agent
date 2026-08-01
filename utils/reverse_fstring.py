
def reverse_fstring(pattern: str, string: str) -> dict[str, str] | None:
  """Reverse f-string.

  Example:

  ```python
  epy.reverse_fstring(
      '/home/{user}/projects/{project}',
      '/home/conchylicultor/projects/menhir'
  ) == {
      'user': 'conchylicultor',
      'project': 'menhir',
  }
  ```

  Args:
    pattern: The f-string pattern (can only contained named group)
    string: The string to search

  Returns:
    The extracted info
  """
  pattern = _pattern_cache(pattern)
  if m := pattern.fullmatch(string):
    return m.groupdict()
  else:
    return None

