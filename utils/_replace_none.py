
def _replace_none(primal_in_aval, maybe_ct):
  if maybe_ct is None:
    return ad_util.Zero(primal_in_aval.to_ct_aval())
  else:
    return maybe_ct

