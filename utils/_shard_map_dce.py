
def _shard_map_dce(used_outputs: list[bool], eqn: core.JaxprEqn
                   ) -> tuple[list[bool], core.JaxprEqn | None]:
  if not any(used_outputs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None
  mesh = eqn.params["mesh"]
  manual_axes = eqn.params["newly_manual_axes"]
  check_vma = eqn.params["check_vma"]
  with (_extend_axis_env(mesh, manual_axes), config._check_vma(check_vma),
        use_abstract_mesh(_as_manual_mesh(mesh, manual_axes))):
    jaxpr, used_inputs = pe.dce_jaxpr(eqn.params['jaxpr'], used_outputs)
  if not any(used_inputs) and not any(used_outputs) and not jaxpr.effects:
    return used_inputs, None
  else:
    _, in_specs = partition_list(used_inputs, eqn.params['in_specs'])
    _, out_specs = partition_list(used_outputs, eqn.params['out_specs'])
    new_params = dict(eqn.params, jaxpr=jaxpr, in_specs=tuple(in_specs),
                      out_specs=tuple(out_specs))
    new_invars = [v for v, used in zip(eqn.invars, used_inputs) if used]
    effs = core.filter_named_axis_effects(
        core.eqn_effects(jaxpr, new_invars), mesh.axis_names)
    new_eqn = pe.new_jaxpr_eqn(
        new_invars,
        [x for x, used in zip(eqn.outvars, used_outputs) if used],
        eqn.primitive, new_params, effs, eqn.source_info, eqn.ctx)
    return used_inputs, new_eqn

