
def _dot_general_remat(policy, lhs, rhs, **params):
  from jax._src.ad_checkpoint import DotsSaveable, primal_left_tangent_right
  dot = partial(dot_general_p.bind, **params)
  out = dot(lhs, rhs)
  if (isinstance(policy, DotsSaveable) and
      policy(dot_general_p, typeof(lhs), typeof(rhs), **params)):
    return out, lambda lhs, rhs: primal_left_tangent_right(out, dot(lhs, rhs))
  return out, dot  # full remat

