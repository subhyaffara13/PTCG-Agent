
def call_ur_rule(prim, ur_rule, out_s, num_out, *avals, **kwargs):
  if ur_rule is not None:
    return ur_rule(*avals, **kwargs)

  if any(a.sharding.spec.unreduced or a.sharding.spec.reduced for a in avals):
    raise NotImplementedError(
        f'unreduced/reduced rule for {prim.name} is not implemented. Please'
        ' file an issue at https://github.com/jax-ml/jax/issues')
  # Only handles explicit mode. No need to handle manual mode here.
  if any(s.spec.unreduced or s.spec.reduced
         for s in ([out_s] if num_out is None else out_s) if s is not None):
    raise NotImplementedError(
        f'unreduced/reduced rule for {prim.name} is not implemented. Please'
        ' file an issue at https://github.com/jax-ml/jax/issues')
  return ((frozenset(), frozenset()) if num_out is None else
          ([frozenset()] * num_out, [frozenset()] * num_out))

