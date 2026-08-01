
def _core_map_discharge_rule(in_avals, out_avals, *args_flat, jaxpr, debug_info, mesh, **kwargs):
  if type(mesh) not in _core_map_mesh_rules:
    raise NotImplementedError(f"Mesh type {type(mesh)} not supported.")
  if jaxpr.constvars:
    # The mapped jaxpr can only close over refs. Closing over anything else,
    # including arrays, is not allowed -- these must be passed into the jaxpr
    # as inputs.
    consts_avals = [
        aval
        for var in jaxpr.constvars
        if not isinstance(aval := var.aval, state.AbstractRef)
    ]
    is_scalar_const_aval = [
        isinstance(aval, jax_core.ShapedArray) and not aval.shape
        for aval in consts_avals
    ]
    if not all(is_scalar_const_aval):
      ctx = jax_core.JaxprPpContext()
      non_scalar_const_avals = [
          aval
          for aval, is_scalar in zip(consts_avals, is_scalar_const_aval)
          if not is_scalar
      ]
      non_scalar_const_pp_avals = ", ".join(
          jax_core.pp_aval(aval, ctx) for aval in non_scalar_const_avals
      )
      raise ValueError(
          "The kernel function in core_map"
          f" {debug_info.func_src_info} captures non-scalar constants"
          f" [{non_scalar_const_pp_avals}]. You should pass them as inputs."
      )
  return _core_map_mesh_rules[type(mesh)](
      in_avals, out_avals, *args_flat, jaxpr=jaxpr, mesh=mesh, **kwargs
  )

