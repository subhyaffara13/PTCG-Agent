
def _pvary_abstract_eval(aval, *, axes):
  _check_axis_names(axes, 'pvary')
  check_unreduced_args([aval], axes, 'pvary')
  assert isinstance(axes, tuple)
  if set(axes).intersection(aval.mat.varying):
    raise ValueError(
        "pvary is a invariant->variant collective. This means that the axis"
        " names mentioned in `axes` passed to `pvary` must not be present in"
        f" `jax.typeof(inp).mat.varying`. Got axes={axes} and"
        f" jax.typeof(inp)={aval}")
  out_vma = aval.mat.varying.union(frozenset(axes))
  return aval.update(sharding=aval.sharding.update(mesh=get_abstract_mesh()),
                     manual_axis_type=aval.mat.update(varying=out_vma))

