
def unop_ur_rule(name, aval, **kwargs):
  reduced = default_unop_reduced_rule(aval)
  if any(getu(aval)):
    raise NotImplementedError(
        f'unreduced rule for {name} is not implemented. Please'
        ' file an issue at https://github.com/jax-ml/jax/issues')
  return frozenset(), reduced

