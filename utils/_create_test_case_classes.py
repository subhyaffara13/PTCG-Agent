
def _create_test_case_classes():
  """Yields one Testing class per game to test."""
  for game_name, game_string in _GAMES_FULL_TREE_TRAVERSAL_TESTS:
    if not re.match(FLAGS.test_only_games, game_string):
      continue
    game = pyspiel.load_game(game_string)
    new_class = type("EnforceAPIFullTree_{}_Test".format(game_name),
                     (EnforceAPIOnFullTreeBase,), {})
    new_class.game_name = game_name
    new_class.game = game
    yield new_class

  for game_name in _GAMES_TO_TEST:
    if not re.match(FLAGS.test_only_games, game_name):
      continue
    game = pyspiel.load_game(game_name)
    new_class = type("EnforceAPIPartialTree_{}_Test".format(game_name),
                     (EnforceAPIOnPartialTreeBase,), {})
    new_class.game_name = game_name
    new_class.game = game
    yield new_class

