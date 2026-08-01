
def try_constant_folding(primitive, tracers, params, out_avals):
  if primitive in const_fold_rules:
    consts_in = [t.get_const() for t in tracers]
    if any(c is not None for c in consts_in):
      return const_fold_rules[primitive](consts_in, params, out_avals)
  return None

