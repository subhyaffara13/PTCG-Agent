
def _get_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, *idx,
    tree):
  del in_avals, out_avals
  y = _get_discharge(x, idx, tree)
  return (None,) * (len(idx) + 1), y

