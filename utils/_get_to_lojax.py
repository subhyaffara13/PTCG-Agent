
def _get_to_lojax(ref, *idx, tree):
  val_ty = core.typeof(ref._refs)
  transforms = tree_util.tree_unflatten(tree, idx)
  if transforms:
    ref = TransformedRef(ref, transforms[:-1])
    idx = transforms[-1]
    return val_ty.ref_get_to_lojax(ref, idx)
  return val_ty.raise_val(*map(ref_get, val_ty.lower_val(ref._refs)))

