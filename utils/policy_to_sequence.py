
def policy_to_sequence(game, policies, infoset_actions_to_seq):
  """Converts a TabularPolicy object for a two-player game.

  The converted policy is its realization-equivalent sequence form one.

  Args:
      game: a two-player open spiel game.
      policies: a TabularPolicy object.
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id.

  Returns:
      A list of numpy arrays, one for each player.
  """
  initial_state = game.new_initial_state()
  sequences = [
      np.ones(len(infoset_actions_to_seq[0])),
      np.ones(len(infoset_actions_to_seq[1]))
  ]
  _policy_to_sequence(initial_state, policies, sequences,
                      infoset_actions_to_seq, [1, 1])
  return sequences

