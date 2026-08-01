
def _choice(n, m):
  rng = np.random.RandomState(42)
  return rng.choice(n, size=m, replace=False)

