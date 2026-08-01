
def _is_optional_game(basename):
  """Returns (bool, game_name or None).

  Args:
    basename: The basename of the file. It is assumed it starts with the game
      name.
  """
  for game_name in _OPTIONAL_GAMES:
    if basename.startswith(game_name):
      return True, game_name
  return False, None

