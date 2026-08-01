
def fwd_bwd_jaxprs(f, *example_args):
  fwd_jaxpr, (y_shape, res_shape) = api.make_jaxpr(
      lambda *args: api.vjp(f, *args), return_shape=True)(*example_args)
  bwd_jaxpr = api.make_jaxpr(lambda res, outs: res(outs))(res_shape, y_shape)
  return fwd_jaxpr, bwd_jaxpr

