
def _while_key_type_signature(eqn):
  cond_jaxpr = eqn.params['cond_jaxpr'].jaxpr
  cond_nconsts = eqn.params['cond_nconsts']
  body_jaxpr = eqn.params['body_jaxpr'].jaxpr
  body_nconsts = eqn.params['body_nconsts']

  cond_signature = jaxpr_type_signature(cond_jaxpr)
  body_signature = jaxpr_type_signature(body_jaxpr)

  # Error if there are sinks among consts.
  if any(np.any(s.mask) for s in cond_signature.sinks if s.idx < cond_nconsts):
    raise KeyReuseError("while_loop cond function leads to key reuse when repeatedly executed: "
                        f"  {cond_signature=}\n"
                        f"  {eqn=}")
  if any(np.any(s.mask) for s in body_signature.sinks if s.idx < body_nconsts):
    raise KeyReuseError("while_loop body function leads to key reuse when repeatedly executed: "
                        f"  {body_signature=}\n"
                        f"  {eqn=}")

  # carry should only consume keys that are sourced on output.
  body_carry_sinks = {s.idx - body_nconsts: s.mask for s in body_signature.sinks if s.idx >= body_nconsts}
  cond_carry_sinks = {s.idx - cond_nconsts: s.mask for s in cond_signature.sinks if s.idx >= cond_nconsts}
  carry_sources = {s.idx: s.mask for s in body_signature.sources}
  # TODO(jakevdp): check masks at each index?
  if not (cond_carry_sinks.keys() <= carry_sources.keys()):
    raise KeyReuseError("while_loop cond function leads to key reuse when repeatedly executed: "
                        f"  {cond_signature=}\n"
                        f"  {eqn=}")
  if not (body_carry_sinks.keys() <= carry_sources.keys()):
    raise KeyReuseError("while_loop body function leads to key reuse when repeatedly executed: "
                        f"  {body_signature=}\n"
                        f"  {eqn=}")
  if body_carry_sinks.keys() & cond_carry_sinks.keys():
    raise KeyReuseError("while_loop cond and body functions both use the same key: "
                        f"  {cond_signature=}\n"
                        f"  {body_signature=}\n"
                        f"  {eqn=}")
  return body_signature

