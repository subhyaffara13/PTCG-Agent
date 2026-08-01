
def _call_hi_primitive_typecheck(_ctx_factory, *in_atoms_flat, _prim):
  in_avals = [x.aval for x in in_atoms_flat]
  if not all(map(core.typematch, in_avals, _prim.in_avals_flat)):
    raise TypeError(f"input type mismatch for {_prim}")
  _prim.check()
  return _prim.out_avals_flat, _prim.effects

