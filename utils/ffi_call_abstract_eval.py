
def ffi_call_abstract_eval(
    *avals_in,
    result_avals: tuple[core.AbstractValue, ...],
    has_side_effect: bool,
    **_,
):
  core.standard_vma_rule('ffi_call', *avals_in)
  effects = {_FfiEffect} if has_side_effect else core.no_effects
  return tuple(r if r is core.abstract_token else
               r.update(sharding=(core.get_cur_mesh_sharding()
                                  if r.sharding.mesh.empty else r.sharding))  # pyrefly: ignore[missing-attribute]
               for r in result_avals), effects

