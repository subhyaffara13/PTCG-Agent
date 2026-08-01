
def _merge_common_consts(
    jaxprs: Sequence[core.ClosedJaxpr],
    all_consts: Sequence[Sequence[Any]]
    ) -> tuple[Sequence[core.ClosedJaxpr], Sequence[Any]]:
  # Jaxprs must share consts, so we concat consts and pad the jaxprs' constvars.
  lens = map(len, all_consts)
  consts = [c for cs in all_consts for c in cs]
  avalqdds = tuple(map(core.cur_aval_qdd, consts))
  num_constss = [len(cs) for cs in all_consts]
  jaxprs = [_pad_constvars(jaxpr, num_consts, avalqdds[:sum(lens[:i])], avalqdds[sum(lens[:i+1]):])
            for i, (jaxpr, num_consts) in enumerate(zip(jaxprs, num_constss))]
  # De-duplicate shared constants.
  const_ids = tuple(id(c) for c in consts)
  seen = set()
  dd_consts = [c for c in consts if id(c) not in seen and not seen.add(id(c))]
  jaxprs = [_dedup_consts(jaxpr, len(consts), const_ids) for jaxpr in jaxprs]
  return jaxprs, dd_consts

