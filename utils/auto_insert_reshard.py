
def auto_insert_reshard(*args):
  if not args:
    return args
  if not config._check_vma.value:
    return insert_reduced_reshard(args)
  if not config.auto_pcast.value:
    return args
  in_vma = [aval.mat.varying if isinstance(aval := typeof(a), ShapedArray)
            else frozenset() for a in args]
  in_reduced = [aval.mat.reduced
                if isinstance(aval := typeof(a), ShapedArray) else frozenset()
                for a in args]
  out_vma = frozenset.union(*in_vma)
  out = []
  for arg, src_vma, src_reduced in zip(args, in_vma, in_reduced):
    if (isinstance(typeof(arg), ShapedArray) and
        (rest_vma := out_vma - src_vma)):
      # TODO(yashkatariya): Handle partial reduced_vary_cast and partial pvary.
      # Will need more changes to pvary to allow such partialness.
      if src_reduced == rest_vma:
        out.append(
            reduced_vary_cast(arg, tuple(n for n in out_vma if n in rest_vma)))
      else:
        out.append(pvary(arg, tuple(n for n in out_vma if n in rest_vma)))
    else:
      out.append(arg)
  return out

