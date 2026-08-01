
def _assert_is_perfect_recall_recursive(state, current_history,
                                        infostate_player_to_history):
  """Raises an AssertionError if the game is not perfect recall.

  The strategy is the following: we traverse the full tree (of states, not
  infostates), and make sure for each node that the history we get for
  the infostate associated to that node, that is is unique with respect to
  the infostate.

  Args:
    state: The current state during the recursive tree traversal.
    current_history: The current list of strictly preceding `SpielState` objects
      that lead to the current `state` (excluded).
    infostate_player_to_history: A dictionnary mapping (infostate string
      representation, current_player) to the list of one instance of actual
      predecessor nodes.
  """

  if not state.is_chance_node() and not state.is_terminal():
    current_player = state.current_player()
    infostate_str = state.information_state_string(current_player)
    key = (infostate_str, current_player)

    if key not in infostate_player_to_history:
      # First time we see the node.
      infostate_player_to_history[key] = list(current_history)
    else:
      previous_history = infostate_player_to_history[key]

      if len(previous_history) != len(current_history):
        raise AssertionError("We found 2 history leading to the same state:\n"
                             "State: {!r}\n"
                             "InfoState str: {}\n"
                             "First history ({} states): {!r}\n"
                             "Second history ({} states): {!r}\n".format(
                                 state.history(), infostate_str,
                                 len(previous_history),
                                 "|".join([str(sa) for sa in previous_history]),
                                 len(current_history),
                                 "|".join([str(sa) for sa in current_history])))

      # Check for `information_state`
      # pylint: disable=g-complex-comprehension
      expected_infosets_history = [(s.information_state_string(current_player),
                                    a)
                                   for s, a in previous_history
                                   if s.current_player() == current_player]
      # pylint: disable=g-complex-comprehension
      infosets_history = [(s.information_state_string(current_player), a)
                          for s, a in current_history
                          if s.current_player() == current_player]

      if expected_infosets_history != infosets_history:
        # pyformat: disable
        raise AssertionError("We found 2 history leading to the same state:\n"
                             "history: {!r}\n"
                             "info_state str: {}\n"
                             "**First history ({} states)**\n"
                             "states: {!r}\n"
                             "info_sets: {!r}\n"
                             "**Second history ({} states)**\n"
                             "Second info_state history: {!r}\n"
                             "Second history: {!r}\n".format(
                                 state.history(),
                                 infostate_str,
                                 len(previous_history),
                                 "|".join([str(sa) for sa in previous_history]),
                                 expected_infosets_history,
                                 len(current_history), infosets_history,
                                 "|".join([str(sa) for sa in current_history])))
        # pyformat: enable

      # Check for `information_state_tensor`
      expected_infosets_history = [
          (s.information_state_tensor(s.current_player()), a)
          for s, a in previous_history
          if s.current_player() == current_player
      ]
      infosets_history = [(s.information_state_tensor(s.current_player()), a)
                          for s, a in current_history
                          if s.current_player() == current_player]

      if infosets_history != expected_infosets_history:
        raise ValueError("The history as tensor in the same infoset "
                         "are different:\n"
                         "History: {!r}\n".format(state.history()))

  # Recursion

  # TODO(author2): We often use a `give me the next node` function and we
  # probably want a utility method for that, which works for all games.
  if state.is_terminal():
    return
  else:
    for action in state.legal_actions():
      state_for_search = state.child(action)
      _assert_is_perfect_recall_recursive(
          state_for_search,
          current_history=current_history + [(state, action)],
          infostate_player_to_history=infostate_player_to_history)

