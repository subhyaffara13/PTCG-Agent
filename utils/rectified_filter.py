
def rectified_filter(player_policies, selection_probabilities, player,
                     effective_number_to_select, solver):
  """Returns every strategy with nonzero selection probability.

  Args:
    player_policies: A list of policies for the current player.
    selection_probabilities: Selection probabilities for 'player_policies'.
    player: Player id.
    effective_number_to_select: Effective number of policies to select.
    solver: PSRO solver instance if kwargs needed.

  Returns:
    selected_policies : List of size 'effective_number_to_select'
      containing selected policies.
    selected_indexes: List of the same shape as selected_policies,
      containing the list indexes of selected policies.
  """
  del effective_number_to_select, solver, player
  selected_indexes = [
      i for i in range(len(player_policies))
      if selection_probabilities[i] > EPSILON_MIN_POSITIVE_PROBA
  ]
  selected_policies = [player_policies[i] for i in selected_indexes]

  return selected_policies, selected_indexes

