
def functional_probabilistic_filter(player_policies, selection_probabilities,
                                    player, effective_number_to_select, solver):
  """Returns effective_number_to_select randomly selected policies by function.

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
  kwargs = solver.get_kwargs()
  # By default, use meta strategies.
  probability_computation_function = kwargs.get(
      "selection_probability_function") or (lambda x: x.get_meta_strategies())

  selection_probabilities = probability_computation_function(solver)[player]
  selected_indexes = list(
      np.random.choice(
          list(range(len(player_policies))),
          effective_number_to_select,
          replace=False,
          p=selection_probabilities))
  selected_policies = [player_policies[i] for i in selected_indexes]
  return selected_policies, selected_indexes

