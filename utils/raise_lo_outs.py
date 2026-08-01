
def raise_lo_outs(hi_avals, lo_outs):
  lo_outs_ = iter(lo_outs)
  hi_outs = [t.raise_val(*it.islice(lo_outs_, len(t.lo_ty()))) for t in hi_avals]
  assert next(lo_outs_, None) is None
  return hi_outs


def raise_lo_outs(hi_avals, lo_outs):
  lo_outs_ = iter(lo_outs)
  hi_outs = [t.raise_val(*it.islice(lo_outs_, len(t.lo_ty()))) for t in hi_avals]
  assert next(lo_outs_, None) is None
  return hi_outs

