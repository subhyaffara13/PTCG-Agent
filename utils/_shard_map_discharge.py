
def _shard_map_discharge(
    in_avals, out_avals, *args, jaxpr, mesh, in_specs, out_specs, check_vma,
    newly_manual_axes):
  inner_mesh = _as_manual_mesh(mesh, newly_manual_axes)
  with (_extend_axis_env(mesh, newly_manual_axes), use_abstract_mesh(inner_mesh),
        config._check_vma(check_vma)):
    discharged_jaxpr = discharge.discharge_state(core.ClosedJaxpr(jaxpr, ()))
  if discharged_jaxpr.consts:
    raise NotImplementedError

  ref_specs = [spec for spec, invar in zip(in_specs, jaxpr.invars)
               if isinstance(invar.aval, AbstractRef)]
  params = dict(
      jaxpr=discharged_jaxpr.jaxpr, out_specs=(*out_specs, *ref_specs)
  )
  params_ = shard_map_p.get_bind_params(params)
  f, = params_.pop('subfuns')
  debug_info = params_['debug_info']
  out_and_ref_vals = shard_map_p.bind(
      *args, subfuns=(f,), mesh=mesh, in_specs=in_specs,
      newly_manual_axes=newly_manual_axes, debug_info=debug_info,
      check_vma=check_vma)
  out_vals, ref_vals = split_list(out_and_ref_vals, [len(jaxpr.outvars)])
  ref_vals_ = iter(ref_vals)
  new_invals = [next(ref_vals_) if isinstance(a, AbstractRef) else None
                for a in in_avals]
  assert next(ref_vals_, None) is None
  return new_invals, out_vals

