
def _addupdate_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, val, *idx,
    tree):
  del in_avals, out_avals
  ans = _addupdate_discharge(x, val, idx, tree)
  return (ans, None) + (None,) * len(idx), []

