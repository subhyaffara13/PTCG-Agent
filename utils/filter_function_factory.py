
def filter_function_factory(filter_function):
  """Returns a function filtering players' strategies wrt.

  'filter_function'.

  This function is used to select which strategy to start training from. As
  such, and in the Rectified Nash Response logic, filter_function expects a
  certain set of arguments:
    - player_policies: The list of policies for the current player.
    - player: The current player id.
    - effective_number_selected: The effective number of policies to select.
    - solver: In case the above arguments weren't enough, the solver instance so
    the filter_function can have more complex behavior.
  And returns the selected policies and policy indexes for the current player.

  Args:
    filter_function: A filter function following the specifications above, used
      to filter which strategy to start training from for each player.

  Returns:
    A filter function on all players.
  """

  def filter_policies(solver, number_policies_selected=1):
    """Filters each player's policies according to 'filter_function'.

    Args:
      solver: The PSRO solver.
      number_policies_selected: The expected number of policies to select. If
        there are fewer policies than 'number_policies_selected', behavior will
        saturate at num_policies.

    Returns:
      used_policies : List of length 'num_players' of lists of length
        min('number_policies_selected', num_policies') containing selected
        policies.
      used_policies_indexes: List of lists of the same shape as used_policies,
        containing the list indexes of selected policies.

    """
    policies = solver.get_policies()
    num_players = len(policies)
    meta_strategy_probabilities = solver.get_meta_strategies()

    used_policies = []
    used_policy_indexes = []
    for player in range(num_players):
      player_policies = policies[player]
      current_selection_probabilities = meta_strategy_probabilities[player]
      effective_number = min(number_policies_selected, len(player_policies))

      used_policy, used_policy_index = filter_function(
          player_policies, current_selection_probabilities, player,
          effective_number, solver)
      used_policies.append(used_policy)
      used_policy_indexes.append(used_policy_index)
    return used_policies, used_policy_indexes

  # Return the created function.
  return filter_policies

