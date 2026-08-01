
def is_user_filename(filename: str) -> bool:
  """Heuristic that guesses the identity of the user's code in a stack trace."""
  return (_include_path_regex().search(filename) is not None
          or _exclude_path_regex().search(filename) is None)

