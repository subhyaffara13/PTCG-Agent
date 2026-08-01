
def igamma_gradx(g, a, x):
  return g * exp(-x + (a - _ones(a)) * log(x) - lgamma(a))

