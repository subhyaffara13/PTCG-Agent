
def _psum_invariant_abstract_eval(name, aval, *, axes):
  assert isinstance(axes, tuple)
  _check_axis_names(axes, 'psum')
  if not set(axes).intersection(aval.mat.varying):
    raise ValueError(
        "psum is a variant->invariant collective. This means that the axis"
        " names mentioned in `axes` passed to `psum` must be present in"
        f" `jax.typeof(inp).mat.varying`. Got axes={axes} and"
        f" jax.typeof(inp).mat.varying={aval.mat.varying}")
  if any(isinstance(a, int) for a in axes):
    raise ValueError(f'psum_invariant does not accept integer axes. Got {axes}')

  named_axes = tuple(axis for axis in axes if not isinstance(axis, int))
  core.check_avals_context_mesh([aval], name)
  check_unreduced_args([aval], axes, name)
  vma = frozenset(a for a in aval.mat.varying if a not in named_axes)
  out_aval = aval.update(manual_axis_type=aval.mat.update(varying=vma))
  return out_aval, {core.NamedAxisEffect(axis) for axis in named_axes}

