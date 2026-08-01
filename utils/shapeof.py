
def shapeof(x):
  return x.shape if isinstance(x, TransformedRef) else core.typeof(x).shape

