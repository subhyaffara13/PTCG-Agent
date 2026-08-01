
def traverse_game_tree(
    game: pyspiel.Game,
    state: pyspiel.State,
    game_stats: GameStats,
    policy: pyspiel.Policy,
    observer: Union[None, chat_game_base.ChatGameObserverBase] = None,
    vectorize: Union[None, Callable[[str, int], np.ndarray]] = None,
):
  """Traverse the game tree and record GameStats in place.

  Args:
    game: pyspiel.Game
    state: initial pyspiel.State
    game_stats: empty GameStats object
    policy: pyspiel Policy
    observer: pyspiel Observer
    vectorize: method to vectorize a string
  """
  if state.is_terminal():
    game_stats.num_terminals += 1
  elif state.is_chance_node():
    game_stats.num_chance_nodes += 1
    for outcome in state.legal_actions():
      child = state.child(outcome)
      traverse_game_tree(game, child, game_stats, policy, observer, vectorize)
  elif state.is_simultaneous_node():
    game_stats.num_simultaneous_nodes += 1
    # TODO(imgemp): need to implement recording data for simultaneous
    # Using joint actions for convenience. Can use legal_actions(player) to
    # and state.apply_actions when walking over individual players
    for joint_action in state.legal_actions():
      child = state.child(joint_action)
      traverse_game_tree(game, child, game_stats, policy, observer, vectorize)
  else:
    game_stats.num_decision_nodes += 1
    if game.get_type().provides_information_state_string:
      sample = record_info_state_data(state, policy, observer, vectorize)
      game_stats.info_state_dict[
          state.information_state_string()] = sample
    for outcome in state.legal_actions():
      child = state.child(outcome)
      traverse_game_tree(game, child, game_stats, policy, observer, vectorize)


def traverse_game_tree(game: pyspiel.Game,
                       state: pyspiel.State,
                       game_stats: GameStats):
  """Traverses the game tree, collecting information about the game."""

  if state.is_terminal():
    game_stats.num_terminals += 1
  elif state.is_chance_node():
    game_stats.num_chance_nodes += 1
    for outcome in state.legal_actions():
      child = state.child(outcome)
      traverse_game_tree(game, child, game_stats)
  elif state.is_simultaneous_node():
    game_stats.num_simultaneous_nodes += 1
    # Using joint actions for convenience. Can use legal_actions(player) to
    # and state.apply_actions when walking over individual players
    for joint_action in state.legal_actions():
      child = state.child(joint_action)
      traverse_game_tree(game, child, game_stats)
  else:
    game_stats.num_decision_nodes += 1
    legal_actions = state.legal_actions()
    if game.get_type().provides_information_state_string:
      game_stats.info_state_dict[
          state.information_state_string()] = legal_actions
    for action in state.legal_actions():
      # print(f"Decision node: \n {state}")
      # print(f"Taking action {action} ({state.action_to_string(action)}")
      child = state.child(action)
      traverse_game_tree(game, child, game_stats)

