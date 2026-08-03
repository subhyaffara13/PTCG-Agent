from typing import Any

def _swap_jvp(primals, tangents, *, args_tree, **params):
  ref_primal, transforms, val_primal, mask = args_tree.unflatten(primals)
  ref_tangent, _, val_tangent, _ = args_tree.unflatten(tangents)
  val_tangent = ad_util.instantiate(val_tangent)
  return (
      swap_p.bind(
          *tree_util.tree_leaves((ref_primal, transforms, val_primal, mask)),
          args_tree=args_tree,
          **params,
      ),
      swap_p.bind(
          *tree_util.tree_leaves((ref_tangent, transforms, val_tangent, mask)),
          args_tree=args_tree,
          **params,
      ),
  )


def _swap_jvp(primals: list[Any], tangents: list[Any], **params: Any):
  ref_primal, x_primal, *idx = primals
  ref_tangent, x_tangent, *_ = tangents
  out_primal = swap_p.bind(ref_primal, x_primal, *idx, **params)
  if isinstance(ref_tangent, ad_util.Zero) and isinstance(x_tangent, ad_util.Zero):
    out_tangent = ad_util.Zero(core.typeof(out_primal).to_tangent_aval())
  elif ref_tangent.aval.kind == "no_grad_no_remat":
    out_tangent = ad_util.Zero(core.typeof(out_primal).to_tangent_aval())
  else:
    if isinstance(ref_tangent, ad_util.Zero):
      raise Exception("performing a set/swap operation with a differentiated "
                      "value on a non-differentiated array reference of type "
                      f"{core.typeof(ref_primal)}. Move the array reference "
                      "to be an argument of the differentiated function?")
    x_tangent = ad_util.instantiate(x_tangent)
    out_tangent = swap_p.bind(ref_tangent, x_tangent, *idx, **params)
  return out_primal, out_tangent

