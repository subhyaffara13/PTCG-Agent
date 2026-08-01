
def generate_all_action_permutations(current_stem, remaining_actions):
  """Return a List of all possible game continuations.

  Return a List of all possible game continuations playing on from the
  current stem and with playing from the set of remaining actions.
  `current_stem` = "" generates all possible playthroughs from the current
  information state.

  Args:
     current_stem: the prior sequence of actions to be completed by the
       remaining actions
     remaining_actions: a 2d array of [subsequent states]x[possible actions]

  Returns:
     An array with each element being the current stem joined with a possible
     permuation of remaining actions
  """
  if not remaining_actions:
    return [np.array(current_stem)]
  else:
    next_actions = remaining_actions[0]
    permutations = []
    for action in next_actions:
      next_stem = current_stem.copy()
      next_stem.append(action)
      next_remaining_actions = remaining_actions[1:]
      prev_permutations = generate_all_action_permutations(
          next_stem, next_remaining_actions
      )
      for i in prev_permutations:
        permutations.append(i)
    return permutations

