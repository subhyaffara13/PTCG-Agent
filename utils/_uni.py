
def _uni(meta_game, per_player_repeats, ignore_repeats=False):
  """Uniform."""
  if ignore_repeats:
    num_policies = meta_game.shape[1:]
    num_dists = np.prod(num_policies)
    meta_dist = np.full(num_policies, 1./num_dists)
  else:
    outs = [ppr / np.sum(ppr) for ppr in per_player_repeats]
    labels = string.ascii_lowercase[:len(outs)]
    comma_labels = ",".join(labels)
    meta_dist = np.einsum("{}->{}".format(comma_labels, labels), *outs)
  return meta_dist, dict()

