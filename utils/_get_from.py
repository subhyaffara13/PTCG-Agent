
def _get_from(aval, axes: tuple[AxisName, ...], name) -> str:
  out = set()
  for a in axes:
    if a in aval.mat.varying:
      out.add('varying')
    elif a in aval.mat.unreduced:
      out.add('unreduced')
    elif a in aval.mat.reduced:
      out.add('reduced')
    else:
      out.add('invarying')

  if len(out) > 1:
    raise ValueError(
        f"{name} can only accept axis_name which corresponds to one of"
        " varying, unreduced, reduced or invarying state of the input. Got"
        f" input type: {aval}, axes: {axes} and input state: {out}")
  o, = out
  return o

