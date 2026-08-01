
def to_concrete_value(x):
  if isinstance(x, Tracer):
    return x.to_concrete_value()
  else:
    return x

