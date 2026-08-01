
def _load_jvp(primals, tangents, args_tree, **params):
  ref_primal, transforms, mask, other_primal = args_tree.unflatten(primals)
  ref_tangent, _, _, other_tangent = args_tree.unflatten(tangents)
  if other_tangent is not None:
    other_tangent = ad_util.instantiate(other_tangent)
  return (
      load_p.bind(
          *tree_util.tree_leaves((ref_primal, transforms, mask, other_primal)),
          args_tree=args_tree,
          **params,
      ),
      load_p.bind(
          *tree_util.tree_leaves(
              (ref_tangent, transforms, mask, other_tangent)
          ),
          args_tree=args_tree,
          **params,
      ),
  )

