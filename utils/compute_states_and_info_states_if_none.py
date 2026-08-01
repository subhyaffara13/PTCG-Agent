
def compute_states_and_info_states_if_none(game,
                                           all_states=None,
                                           state_to_information_state=None):
  """Returns all_states and/or state_to_information_state for the game.

  To recompute everything, pass in None for both all_states and
  state_to_information_state. Otherwise, this function will use the passed in
  values to reconstruct either of them.

  Args:
    game: The open_spiel game.
    all_states: The result of calling get_all_states.get_all_states. Cached for
      improved performance.
    state_to_information_state: A dict mapping state.history_str() to
      state.information_state for every state in the game. Cached for improved
      performance.
  """
  if all_states is None:
    all_states = get_all_states.get_all_states(
        game,
        depth_limit=-1,
        include_terminals=False,
        include_chance_states=False)

  if state_to_information_state is None:
    state_to_information_state = {
        state: all_states[state].information_state_string()
        for state in all_states
    }

  return all_states, state_to_information_state


def compute_states_and_info_states_if_none(game,
                                           all_states=None,
                                           state_to_information_state=None):
  """Returns all_states and/or state_to_information_state for the game.

  To recompute everything, pass in None for both all_states and
  state_to_information_state. Otherwise, this function will use the passed in
  values to reconstruct either of them.

  Args:
    game: The open_spiel game.
    all_states: The result of calling get_all_states.get_all_states. Cached for
      improved performance.
    state_to_information_state: A dict mapping str(state) to
      state.information_state for every state in the game. Cached for improved
      performance.
  """
  if all_states is None:
    all_states = get_all_states.get_all_states(
        game,
        depth_limit=-1,
        include_terminals=False,
        include_chance_states=False)

  if state_to_information_state is None:
    state_to_information_state = {
        state: all_states[state].information_state_string()
        for state in all_states
    }

  return all_states, state_to_information_state

