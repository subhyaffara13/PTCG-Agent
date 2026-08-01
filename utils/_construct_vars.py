
def _construct_vars(state, infosets, infoset_actions_to_seq,
                    infoset_action_maps, infoset_parent_map, chance_reach,
                    parent_is_keys, parent_isa_keys, payoff_dict,
                    infoset_actions_children):
  """Recursively builds maps and the sequence form payoff matrix.

  Args:
      state: pyspiel (OpenSpiel) state
      infosets: a list of dicts, one per player, that maps infostate to an id.
        The dicts are filled by this function and should initially only
        contain root values.
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id. The dicts are filled by
        this function and should initially only contain the root values.
      infoset_action_maps: a list of dicts, one per player, that maps each
        info_state to a list of (infostate, action) string.
      infoset_parent_map: a list of dicts, one per player, that maps each
        info_state to an (infostate, action) string.
      chance_reach: the contribution of chance's reach probability (should
        start at 1).
      parent_is_keys: a list of parent information state keys for this state
      parent_isa_keys: a list of parent (infostate, action) keys
      payoff_dict: a dict that maps sequences of players' (infostate, action)
        tuples, e.g., ((infostate, action), ...) to the chance weighted reward.
      infoset_actions_children: a list of dicts, one for each player, mapping
        (infostate, action) keys to reachable infostates for each player
  """

  if state.is_terminal():
    returns = state.returns()
    idx = tuple(parent_isa_keys_i for parent_isa_keys_i in parent_isa_keys)
    payoff_dict.setdefault(idx, 0)
    payoff_dict[idx] += np.asarray(returns) * chance_reach
    return

  if state.is_chance_node():
    for action, prob in state.chance_outcomes():
      new_state = state.child(action)
      _construct_vars(new_state, infosets, infoset_actions_to_seq,
                      infoset_action_maps, infoset_parent_map,
                      prob * chance_reach, parent_is_keys, parent_isa_keys,
                      payoff_dict, infoset_actions_children)
    return

  player = state.current_player()
  info_state = state.information_state_string(player)
  legal_actions = state.legal_actions(player)

  # Add to the infostate maps
  if info_state not in infosets[player]:
    infosets[player][info_state] = len(infosets[player])
  if info_state not in infoset_action_maps[player]:
    infoset_action_maps[player][info_state] = []

  # Add to infoset to parent infoset action map
  if info_state not in infoset_parent_map[player]:
    infoset_parent_map[player][info_state] = parent_isa_keys[player]

  # add as child to parent
  if parent_isa_keys[player] in infoset_actions_children[player]:
    if info_state not in infoset_actions_children[player][
        parent_isa_keys[player]]:
      infoset_actions_children[player][parent_isa_keys[player]].append(
          info_state)
  else:
    infoset_actions_children[player][parent_isa_keys[player]] = [info_state]

  new_parent_is_keys = parent_is_keys[:]
  new_parent_is_keys[player] = info_state

  for action in legal_actions:
    isa_key = get_isa_key(info_state, action)
    if isa_key not in infoset_actions_to_seq[player]:
      infoset_actions_to_seq[player][isa_key] = len(
          infoset_actions_to_seq[player])
    if isa_key not in infoset_action_maps[player][info_state]:
      infoset_action_maps[player][info_state].append(isa_key)

    new_parent_isa_keys = parent_isa_keys[:]
    new_parent_isa_keys[player] = isa_key
    new_state = state.child(action)
    _construct_vars(new_state, infosets, infoset_actions_to_seq,
                    infoset_action_maps, infoset_parent_map, chance_reach,
                    new_parent_is_keys, new_parent_isa_keys, payoff_dict,
                    infoset_actions_children)

