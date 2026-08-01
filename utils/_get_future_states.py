
def _get_future_states(possibilities, state, reach=1.0):
  """Does a lookahead over chance nodes to all next states after (s,a).

  Also works if there are no chance nodes (i.e. base case).

  Arguments:
    possibilities:  an empty list, that will be filled with (str(next_state),
      transition probability) pairs for all possible next states
    state: the state following some s.apply_action(a), can be a chance node
    reach: chance reach probability of getting to this point from (s,a)
  Returns: nothing.
  """
  if not state.is_chance_node() or state.is_terminal():
    # Base case
    possibilities.append((str(state), reach))
  else:
    assert state.is_chance_node()
    for outcome, prob in state.chance_outcomes():
      next_state = state.child(outcome)
      _get_future_states(possibilities, next_state, reach * prob)

