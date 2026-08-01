
def _policy_to_sequence(state, policies, sequences, infoset_actions_to_seq,
                        parent_seq_val):
  """Converts a TabularPolicy object to its equivalent sequence form.

  This method modifies the sequences inplace and should not be called directly.

  Args:
      state: an openspiel state.
      policies: a TabularPolicy object.
      sequences: list of numpy arrays to be modified.
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id.
      parent_seq_val: list of parent sequence values, this method should be
        called with initial value of [1,1].
  """

  if state.is_terminal():
    return

  if state.is_chance_node():
    for action, _ in state.chance_outcomes():
      new_state = state.child(action)
      _policy_to_sequence(new_state, policies, sequences,
                          infoset_actions_to_seq, parent_seq_val)
    return

  player = state.current_player()
  info_state = state.information_state_string(player)
  legal_actions = state.legal_actions(player)
  state_policy = policies.policy_for_key(info_state)
  for action in legal_actions:
    isa_key = get_isa_key(info_state, action)
    # update sequence form
    sequences[player][infoset_actions_to_seq[player]
                      [isa_key]] = parent_seq_val[player] * state_policy[action]
    new_parent_seq_val = parent_seq_val[:]
    new_parent_seq_val[player] = sequences[player][
        infoset_actions_to_seq[player][isa_key]]
    new_state = state.child(action)
    _policy_to_sequence(new_state, policies, sequences, infoset_actions_to_seq,
                        new_parent_seq_val)

