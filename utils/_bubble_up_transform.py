import functools

def _bubble_up_transform(
    ctx: LoweringRuleContext,
    aval: jax_core.AbstractValue,
    transforms: Sequence[state_types.Transform],
    transforms_avals: Sequence[state_types.Transform],
    t: T,
    t_aval: T,
) -> tuple[T, T, list[state_types.Transform], list[state_types.Transform]]:
  new_transforms_rev = []
  new_transforms_avals_rev = []
  for transform, transform_aval in reversed(zip(transforms, transforms_avals)):
    avals = (transform_aval, t_aval)
    (t, new_transform), (t_aval, new_transform_aval) = _lower_fn_with_avals(
        functools.partial(_commute_transform, aval), avals
    )(ctx, transform, t)
    if not isinstance(new_transform, gpu_core.IdentityTransform):
      new_transforms_rev.append(new_transform)
      new_transforms_avals_rev.append(new_transform_aval)
  new_transforms_rev.reverse()
  new_transforms_avals_rev.reverse()
  return (
      t,
      t_aval,
      new_transforms_rev,
      new_transforms_avals_rev,
  )

