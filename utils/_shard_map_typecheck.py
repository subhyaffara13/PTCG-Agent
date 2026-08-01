
def _shard_map_typecheck(_, *in_atoms, jaxpr, mesh, in_specs, out_specs,
                         check_vma, newly_manual_axes):
  # TODO(mattjj,parkers): check auto
  for v, x, in_spec in zip(jaxpr.invars, in_atoms, in_specs):
    sharded_aval = shard_aval(mesh, newly_manual_axes, check_vma, in_spec, x.aval)
    if not core.typecompat(v.aval, sharded_aval):
      raise core.JaxprTypeError("shard_map argument avals not compatible with "
                                "jaxpr binder avals and in_specs")
  with _extend_axis_env(mesh, newly_manual_axes), config._check_vma(check_vma):
    core.check_jaxpr(jaxpr)
  if check_vma:
    for v, os in zip(jaxpr.outvars, out_specs):
      if isinstance(os, P) and not _valid_repeats(mesh, v.aval.mat, os):
        raise core.JaxprTypeError(
            "shard_map can't prove output is sufficiently replicated")
  out_avals_sharded = [x.aval for x in jaxpr.outvars]
  out_avals = map(partial(unshard_aval, mesh, check_vma), out_specs,
                  out_avals_sharded)
  effs = core.filter_named_axis_effects(core.positional_effects(jaxpr),
                                        mesh.axis_names)
  return out_avals, effs

