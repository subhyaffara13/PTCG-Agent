
def _rd(meta_game, per_player_repeats, ignore_repeats=False):
  """Random dirichlet."""
  ignore_repeats = True
  if ignore_repeats:
    num_policies = meta_game.shape[1:]
    alpha = np.ones(num_policies)
  else:
    outs = [ppr for ppr in per_player_repeats]
    labels = string.ascii_lowercase[:len(outs)]
    comma_labels = ",".join(labels)
    alpha = np.einsum("{}->{}".format(comma_labels, labels), *outs)
  meta_dist = np.reshape(
      np.random.dirichlet(alpha.flat), alpha.shape).astype(np.float64)
  return meta_dist, dict()

