
def add_tangents(x, y):
  if type(x) is Zero:
    return y
  elif type(y) is Zero:
    return x
  else:
    return add_jaxvals(x, y)

