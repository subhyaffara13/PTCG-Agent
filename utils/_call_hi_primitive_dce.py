
def _call_hi_primitive_dce(used_outs_flat, eqn):
  _prim = eqn.params['_prim']
  used_out = tree_unflatten(_prim.out_tree, used_outs_flat)
  used_ins, produced_outs, new_prim = _prim.dce(used_out)
  if new_prim is None:
    return [False] * len(eqn.invars), None
  used_ins_flat = broadcast_prefix(used_ins, _prim.in_avals)
  produced_outs_flat = broadcast_prefix(produced_outs, _prim.out_aval)
  new_invars = [x for x, u in zip(eqn.invars, used_ins_flat) if u]
  new_outvars = [v for v, u in zip(eqn.outvars, produced_outs_flat) if u]
  new_eqn = eqn.replace(invars=new_invars, outvars=new_outvars,
                        params=dict(_prim=new_prim))
  return used_ins_flat, new_eqn

