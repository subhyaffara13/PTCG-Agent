
def _eval_jaxpr_batching_rule(axis_data, args, dims, *, jaxpr):
  batched = [d is not None for d in dims]
  new_jaxpr, out_batched = batching.batch_jaxpr(jaxpr, axis_data, batched, False)
  new_args = [batching.moveaxis(x, d, 0)
              if d is not None and d != 0 else x
              for x, d in zip(args, dims)]
  outs = eval_jaxpr_p.bind(*new_args, jaxpr=new_jaxpr)
  out_dims = [0 if b else None for b in out_batched]
  return outs, out_dims

