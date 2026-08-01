
def construct_constraint_vars(infoset_parent_map, infoset_actions_to_seq,
                              infoset_action_maps):
  """Construct useful sequence form variables from game.

  Args:
      infoset_parent_map: a list of dicts, one per player, that maps each
        info_state to an (infostate, action) string.
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id.
      infoset_action_maps: a list of dicts, one per player, that maps each
        info_state to a list of (infostate, action) string.

  Returns:
      A dict mapping player to a tuple containing a numpy array of coefficients,
      each of dimension # of player sequences, as well as a sparse vector
      containing the constants, i.e., dict[player] = (A, b) as in Ax = b.
  """
  npl = len(infoset_actions_to_seq)
  constraint_dict = {}

  for player in range(npl):
    num_seqs = len(infoset_actions_to_seq[player].values())

    root_con = np.zeros(num_seqs)
    root_con[0] = 1.0
    constraints = [root_con]

    for info_state in infoset_action_maps[player]:
      if is_root(info_state, player):
        continue

      parent_isa_key = infoset_parent_map[player][info_state]
      parent_seq_id = infoset_actions_to_seq[player][parent_isa_key]

      # seq ids for children
      children_isa_keys = infoset_action_maps[player][info_state]
      children_seq_ids = [
          infoset_actions_to_seq[player][isa_key]
          for isa_key in children_isa_keys
      ]

      constraint = np.zeros(num_seqs)
      constraint[parent_seq_id] = -1.0
      constraint[children_seq_ids] = 1.0
      constraints.append(constraint)

    constant = np.zeros(len(constraints))
    constant[0] = 1.0
    constraint_dict[player] = (np.stack(constraints), constant)

  return constraint_dict

