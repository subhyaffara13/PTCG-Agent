
def _swap_to_lojax(ref, val, *idx, tree):
  ref_val_ty = core.typeof(ref._refs)
  val_ty = core.typeof(val)
  transforms = tree_util.tree_unflatten(tree, idx)
  if transforms:
    ref = TransformedRef(ref, transforms[:-1])
    idx = transforms[-1]
    return ref_val_ty.ref_swap_to_lojax(ref, val, idx)
  lo_refs = ref_val_ty.lower_val(ref._refs)
  lo_vals = val_ty.lower_val(val)
  outs = [ref_swap(lo_ref, idx, lo_val) for lo_ref, lo_val
          in zip(lo_refs, lo_vals)]
  return val_ty.raise_val(*outs)

