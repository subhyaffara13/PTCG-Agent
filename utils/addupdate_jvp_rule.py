from typing import Any

def addupdate_jvp_rule(primals: list[Any], tangents: list[Any], **params: Any):
  ref_primal, x_primal, *idx = primals
  ref_tangent, x_tangent, *_ = tangents
  x_tangent = ad_util.instantiate(x_tangent)
  if ref_tangent.aval.kind != "no_grad_no_remat":
    addupdate_p.bind(ref_primal, x_primal, *idx, **params)
    addupdate_p.bind(ref_tangent, x_tangent, *idx, **params)
  return [], []

