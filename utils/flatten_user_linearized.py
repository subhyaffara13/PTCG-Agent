
def flatten_user_linearized(prim, residuals, *tangents_flat):
  tangents = tree_unflatten(prim.in_tree, tangents_flat)
  tangents_out = prim.linearized(residuals, *tangents)
  tangents_out_flat = tree_leaves_checked(prim.out_tree, tangents_out)
  return tangents_out_flat

