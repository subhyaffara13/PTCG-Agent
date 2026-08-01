
def sequence_to_policy(sequences, game, infoset_actions_to_seq,
                       infoset_action_maps):
  """Convert sequence form policies to the realization-equivalent tabular ones.

  Args:
      sequences: list of two sequence form policies, one for each player.
      game: a spiel game with two players.
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id.
      infoset_action_maps: a list of dicts, one per player, that maps each
        info_state to a list of (infostate, action) string.

  Returns:
      A TabularPolicy object.
  """

  policies = policy.TabularPolicy(game)
  for player in range(2):
    for info_state in infoset_action_maps[player]:
      if is_root(info_state, player):
        continue

      state_policy = policies.policy_for_key(info_state)
      total_weight = 0
      num_actions = 0

      for isa_key in infoset_action_maps[player][info_state]:
        total_weight += sequences[player][infoset_actions_to_seq[player]
                                          [isa_key]]
        num_actions += 1

      unif_pr = 1.0 / num_actions
      for isa_key in infoset_action_maps[player][info_state]:
        rel_weight = sequences[player][infoset_actions_to_seq[player][isa_key]]
        _, action_str = isa_key.split(_DELIMITER)
        action = int(action_str)
        pr_action = rel_weight / total_weight if total_weight > 0 else unif_pr
        state_policy[action] = pr_action
  return policies

