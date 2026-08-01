
def _find_downstream(
    jaxpr: jax_core.Jaxpr, in_used: Sequence[bool]
) -> tuple[bool, ...]:
  # TODO(sharadmv): We use partial_eval to query downstream dependencies which
  # is not an officially sanctioned way to do so, since PE is really used for
  # AD. In the future, we should have a special Jaxpr API that queries this.
  discharged_jaxpr, *_ = fuser_utils.discharge_state(jaxpr)
  _, _, out_used, *_ = pe.partial_eval_jaxpr_custom(
      discharged_jaxpr,
      in_unknowns=in_used,
      in_inst=in_used,
      ensure_out_unknowns=False,
      ensure_out_inst=False,
      saveable=lambda *_, **__: False,
  )
  # NOTE: out_used[:len(jaxpr.outvars)] reports whether or not the the original
  # outputs depend on the inputs for which `in_used` is True.
  # out_used[len(jaxpr.outvars):] reports whether or not the new outputs
  # (updates for discharged Refs) depend on thse inputs.
  return tuple(out_used)

