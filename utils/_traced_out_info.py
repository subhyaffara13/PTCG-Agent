
def _traced_out_info(self):
  out_shardings = [None if isinstance(s, UnspecifiedValue) else s
                   for s in self._params['out_shardings']]
  out_layouts = [None if isinstance(l, AutoLayoutSingleton) else l
                 for l in self._params['out_layouts']]
  out = []
  for a, out_s, out_l in zip(self.jaxpr.out_avals, out_shardings, out_layouts):
    if isinstance(a, core.ShapedArray):
      s = ((a.sharding if a.sharding.mesh._are_all_axes_explicit_or_manual
            else out_s) if out_s is None else out_s)
      out.append(
          core.ShapeDtypeStruct(
              a.shape, a.dtype, sharding=Format(out_l, s),
              weak_type=a.weak_type,
              manual_axis_type=(a.mat if config._check_vma.value else None)))
    else:
      out.append(a)
  return tree_util.tree_unflatten(self.out_tree, out)

