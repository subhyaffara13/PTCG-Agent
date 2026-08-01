
def _get_repeat_factor(action_repeats):
  """Returns the repeat factors for the game."""
  num_players = len(action_repeats)
  out_labels = string.ascii_lowercase[:len(action_repeats)]
  in_labels = ",".join(out_labels)
  repeat_factor = np.ravel(np.einsum(
      "{}->{}".format(in_labels, out_labels), *action_repeats))
  indiv_repeat_factors = []
  for player in range(num_players):
    action_repeats_ = [
        np.ones_like(ar) if player == p else ar
        for p, ar in enumerate(action_repeats)]
    indiv_repeat_factor = np.ravel(np.einsum(
        "{}->{}".format(in_labels, out_labels), *action_repeats_))
    indiv_repeat_factors.append(indiv_repeat_factor)
  return repeat_factor, indiv_repeat_factors

