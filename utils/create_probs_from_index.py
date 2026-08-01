
def create_probs_from_index(indices, current_policy):
  path_to_state = []
  if indices is None or not indices:
    return []
  for index in indices:
    strat_dict = array_to_strat_dict(
        current_policy.action_probability_array[index[1]], index[0]
    )
    path_to_state.append(strat_dict)
  return path_to_state

