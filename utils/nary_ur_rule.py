
def nary_ur_rule(name, *avals, **params):
  reduced = default_nary_reduced_rule(*avals, **params)
  if any(getu(a) for a in avals):
    raise NotImplementedError(
        f'unreduced rule for {name} is not implemented. Please'
        ' file an issue at https://github.com/jax-ml/jax/issues')
  return frozenset(), reduced

