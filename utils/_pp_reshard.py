
def _pp_reshard(eqn, ctx, settings):
  return core._pp_eqn(eqn.replace(params={}), ctx, settings)

