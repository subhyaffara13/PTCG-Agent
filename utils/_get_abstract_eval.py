
def _get_abstract_eval(ref_aval: AbstractRef, *args,
                       tree):
  transforms = tree_util.tree_unflatten(tree, args)
  if transforms and ref_aval.inner_aval.is_high:
    # TODO(mattjj): aval.is_high does not imply the existence of ref_get_abstract_aval.
    return ref_aval.inner_aval.ref_get_abstract_eval(ref_aval, *args, tree=tree)  # pyrefly: ignore[missing-attribute]
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`get` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    out_aval = transform_type(transforms, ref_aval.inner_aval)
  else:
    if transforms:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
    out_aval = ref_aval.inner_aval
  return (out_aval, {ReadEffect(0)})

