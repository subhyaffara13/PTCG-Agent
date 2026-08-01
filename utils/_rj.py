
def _rj(meta_game, per_player_repeats, ignore_repeats=False):
  """Random joint."""
  ignore_repeats = True
  pvals, _ = _uni(
      meta_game, per_player_repeats, ignore_repeats=ignore_repeats)
  meta_dist = np.reshape(
      np.random.multinomial(1, pvals.flat), pvals.shape).astype(np.float64)
  return meta_dist, dict()

