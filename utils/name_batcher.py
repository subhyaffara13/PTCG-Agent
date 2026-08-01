
def name_batcher(args, dims, *, name):
  (x,), (d,) = args, dims
  return name_p.bind(x, name=name), d

