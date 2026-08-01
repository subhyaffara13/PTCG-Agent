
def project_accums(args):
  result, specs = [], []
  for x in args:
    if isinstance(x, ValAccum):
      specs.append((ValAccum, x.aval))
    elif isinstance(x, RefAccum):
      result.append(x.inst().ref)
      specs.append((RefAccum, x.aval))
    elif isinstance(x, NullAccum):
      specs.append((NullAccum, x.aval))
    else:
      result.append(x)
      specs.append((None, typeof(x)))
  return result, tuple(specs)

