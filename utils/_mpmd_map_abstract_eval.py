
def _mpmd_map_abstract_eval(
    *in_avals,
    jaxprs,
    out_avals,
    input_output_aliases,
    interpret,
    compiler_params,
    meshes,
    **params,
):
  del params, compiler_params  # Unused.

  effs = {*pallas_core.get_interpret_effects(interpret)}
  all_mesh_axis_names = {
      eff.name
      for jaxpr in jaxprs
      for eff in jaxpr.effects
      if isinstance(eff, jax_core.NamedAxisEffect)
  }
  for mesh, jaxpr in zip(meshes, jaxprs):
    for eff in jaxpr.effects:
      if mesh.discharges_effect(eff):
        continue
      if pallas_core.kernel_local_effects.contains(eff):
        continue
      if isinstance(eff, effects.JaxprInputEffect):
        # We emit an effect if we have a Ref input that has been written to in
        # the kernel.
        assert not jaxpr.constvars
        index = jaxpr.invars.index(eff.input)
        if index < len(in_avals) and isinstance(
            in_avals[index], state.AbstractRef
        ):
          effs.add(eff.replace(index))
        continue
      if not isinstance(eff, jax_core.NamedAxisEffect):
        effs.add(eff)
        continue
      if eff.name not in all_mesh_axis_names:
        effs.add(eff)

  # TODO(slebedev): Handle pinned buffers as in ``pallas_call``.
  outin_aliases = {
      out_idx: in_idx for in_idx, out_idx in input_output_aliases.items()
  }
  out_avals = [
      in_avals[outin_aliases[out_idx]] if out_idx in outin_aliases else a
      for out_idx, a in enumerate(out_avals)
  ]
  return out_avals, effs

