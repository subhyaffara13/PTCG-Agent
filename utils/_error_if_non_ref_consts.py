
def _error_if_non_ref_consts(consts, debug_info):
  consts_avals = [
      aval
      for c in consts
      if not isinstance(aval := jax_core.typeof(c), state.AbstractRef)
  ]
  non_scalar_consts_avals = [
      aval
      for aval in consts_avals
      if not (isinstance(aval, jax_core.ShapedArray) and not aval.shape)
  ]
  if non_scalar_consts_avals:
    ctx = jax_core.JaxprPpContext()
    pp_consts_avals = ", ".join(
        jax_core.pp_aval(aval, ctx) for aval in non_scalar_consts_avals
    )
    raise ValueError(
        "The kernel function in the mpmd_map"
        f" {debug_info.func_src_info} captures non-Ref constants"
        f" [{pp_consts_avals}]. You should pass them as inputs."
    )

