from typing import Any

def _get_jvp(primals: list[Any], tangents: list[Any], **params: Any):
  ref_primal, *idx = primals
  ref_tangent, *_ = tangents
  out_primal = get_p.bind(ref_primal, *idx, **params)
  if isinstance(ref_tangent, ad_util.Zero):
    out_tangent = ad_util.Zero(core.typeof(out_primal).to_tangent_aval())
  else:
    out_tangent = get_p.bind(ref_tangent, *idx, **params)
  return out_primal, out_tangent

