
def partial_eval_jaxpr_custom(
    jaxpr: Jaxpr,
    in_unknowns: Sequence[bool],
    in_inst: bool | Sequence[bool],
    ensure_out_unknowns: bool | Sequence[bool],
    ensure_out_inst: bool | Sequence[bool],
    saveable: Callable[..., RematCases_],
  ) -> tuple[Jaxpr, Jaxpr, list[bool], list[bool], int]:
  *outs, num_res_ref = partial_eval_jaxpr_stateful(
      jaxpr, in_unknowns, in_inst, ensure_out_unknowns, ensure_out_inst, saveable)
  if num_res_ref:
    raise ValueError("Cannot use `partial_eval_jaxpr_custom` with stateful jaxprs.")
  return *outs,  # pyrefly: ignore[bad-return]

