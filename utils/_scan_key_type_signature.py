
def _scan_key_type_signature(eqn):
  jaxpr = eqn.params['jaxpr'].jaxpr
  num_consts = eqn.params['num_consts']
  num_carry = eqn.params['num_carry']
  signature = jaxpr_type_signature(jaxpr)

  # scan body should not consume key in constants
  if any(np.any(s.mask) for s in signature.sinks if s.idx < num_consts):
    raise KeyReuseError("scan body function leads to key reuse when repeatedly executed, "
                        "because key constants are repeatedly consumed:\n"
                        f"  {signature=}\n"
                        f"  {eqn=}\n"
                        f"  {jaxpr=}")

  # scan carry should only consume keys that are sourced on output.
  carry_sinks = {s.idx - num_consts: s.mask for s in signature.sinks
                 if 0 <= s.idx - num_consts < num_carry and np.any(s.mask)}
  carry_sources = {s.idx: s.mask for s in signature.sources
                   if 0 <= s.idx < num_carry and np.any(s.mask)}
  if not set(carry_sinks).issubset(set(carry_sources)):  # TODO(jakevdp): check that masks match
    raise KeyReuseError("scan body function leads to key reuse when repeatedly executed, "
                        "because consumed inputs don't match sourced outputs:\n"
                        f"  {signature=}\n"
                        f"  {eqn=}\n"
                        f"  {jaxpr=}")
  return signature

