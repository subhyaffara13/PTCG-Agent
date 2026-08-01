
def accum_typeof(x):
  if isinstance(x, GradAccum):
    return x.aval
  else:
    return typeof(x)

