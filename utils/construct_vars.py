
def construct_vars(game):
  """Construct useful sequence from variables from game.

  Args:
      game: The spiel game to solve (must be zero-sum, sequential, and have
        chance node of deterministic or explicit stochastic).

  Returns:
      An 8 tuple of sequence form variables from _construct_vars by
      recursively
      traversing the game tree.

  """

  initial_state = game.new_initial_state()
  npl = game.num_players()

  empty_is_keys = [f"***EMPTY_INFOSET_P{player}***" for player in range(npl)]
  empty_isa_keys = [
      f"***EMPTY_INFOSET_ACTION_P{player}***" for player in range(npl)
  ]

  # initialize variables
  infosets = [{empty_is_keys[p]: 0} for p in range(npl)]
  infoset_actions_to_seq = [{empty_isa_keys[p]: 0} for p in range(npl)]
  infoset_action_maps = [
      {empty_is_keys[p]: [empty_isa_keys[p]]} for p in range(npl)
  ]

  # infoset_action_maps = [{}, {}]
  payoff_dict = dict()

  infoset_parent_map = [{empty_isa_keys[p]: None} for p in range(npl)]
  infoset_actions_children = [{empty_isa_keys[p]: []} for p in range(npl)]

  _construct_vars(initial_state, infosets, infoset_actions_to_seq,
                  infoset_action_maps, infoset_parent_map, 1.0,
                  empty_is_keys[:], empty_isa_keys[:],
                  payoff_dict, infoset_actions_children)

  payoff_mat = _construct_numpy_vars(payoff_dict, infoset_actions_to_seq)
  return (infosets, infoset_actions_to_seq,
          infoset_action_maps, infoset_parent_map,
          payoff_mat, infoset_actions_children)

