
def _construct_numpy_vars(payoff_dict, infoset_actions_to_seq):
  """Convert sequence form payoff dict to numpy array.

  Args:
      payoff_dict: a dict that maps sequences of players' (infostate, action)
        tuples, e.g., ((infostate, action), ...) to the chance weighted reward.
      infoset_actions_to_seq: a list of dicts, one per player, that maps a
        string of (infostate, action) pair to an id.

  Returns:
      A numpy array corresponding to the chance weighted rewards
      i.e. the sequence form payoff tensor.

  """
  npl = len(infoset_actions_to_seq)
  pls = range(npl)  # player list
  sequence_sizes = tuple(len(infoset_actions_to_seq[i]) for i in pls)
  payoff_tensor = np.zeros((npl,) + sequence_sizes)
  for player_isa_seqs, payoffs in payoff_dict.items():
    idx = tuple(infoset_actions_to_seq[i][player_isa_seqs[i]] for i in pls)
    payoff_tensor[(slice(None),) + idx] = np.asarray(payoffs)
  return payoff_tensor

