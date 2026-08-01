
def get_l1_distribution_dist(mu1, mu2):
  mu1d = mu1.distribution
  mu2d = mu2.distribution
  states = set(list(mu1d.keys()) + list(mu2d.keys()))
  return sum([abs(mu1d.get(a, 0.0) - mu2d.get(a, 0.0)) for a in states
             ]) * FLAGS.dt / FLAGS.horizon

