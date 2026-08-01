
def _select_jvp(primals, tangents):
  which, *case_primals = primals
  case_tangents = tangents[1:]
  out = select_n(which, *case_primals)
  if all(type(t) is ad_util.Zero for t in case_tangents):
    out_dot = ad_util.Zero(case_tangents[0].aval)
  else:
    z = _zeros(next(t for t in case_tangents if type(t) is not ad_util.Zero))
    case_tangents = [z if type(t) is ad_util.Zero else t for t in case_tangents]
    out_dot = select_n(which, *case_tangents)
  return out, out_dot

