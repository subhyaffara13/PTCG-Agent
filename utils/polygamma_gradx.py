
def polygamma_gradx(g, m, x):
  return g * polygamma(add(m, _const(m, 1)), x)

