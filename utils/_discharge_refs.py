
def _discharge_refs(
    jaxpr: core.ClosedJaxpr
) -> tuple[core.ClosedJaxpr, Sequence[int | None], MutationData]:
  from jax._src.state.discharge import discharge_state  # pyrefly: ignore[missing-import]
  jaxpr, in_mut = _move_mutable_consts(jaxpr)
  new_jaxpr = discharge_state(jaxpr)
  count = it.count(len(jaxpr.out_avals))  # new outputs are appended to the end
  inout_map = {i: next(count) for i, a in enumerate(jaxpr.in_avals)
               if isinstance(a, AbstractRef)}
  outin_map = {j: i for i, j in inout_map.items()}
  inout_aliases = tuple(map(inout_map.get, range(len(new_jaxpr.in_avals))))
  out_mut = list(map(outin_map.get, range(len(new_jaxpr.out_avals))))
  return new_jaxpr, inout_aliases, MutationData(in_mut, out_mut)

