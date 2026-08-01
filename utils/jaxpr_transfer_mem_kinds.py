
def jaxpr_transfer_mem_kinds(jaxpr: core.Jaxpr):
  out = []
  for eqn in jaxpr.eqns:
    if eqn.primitive is dispatch.device_put_p:
      out.extend(d for d in eqn.params['devices']
                 if isinstance(d, core.MemorySpace))
    elif eqn.primitive.name == 'compute_on':
      out.extend(o for o in eqn.params['out_memory_spaces'])
    elif eqn.primitive.name == 'call_exported':
      out.extend(aval.memory_space for aval in eqn.params['exported'].out_avals)

  for subjaxpr in core.subjaxprs(jaxpr):
    out.extend(jaxpr_transfer_mem_kinds(subjaxpr))
  return out

