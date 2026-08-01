
def _discharge_refs_jaxpr(closed_jaxpr, in_shardings, in_layouts,
                          donated_invars, out_shardings, out_layouts):
  if (any(isinstance(e, RefEffect) for e in closed_jaxpr.effects) or
      any(isinstance(a, AbstractRef) for a in closed_jaxpr.in_avals)):
    closed_jaxpr, inout_aliases, mut = _discharge_refs(closed_jaxpr)
    in_shardings = (*in_shardings, *(
        pjit.finalize_arg_sharding(c.sharding, c.committed) for c in mut.in_mut))
    in_layouts = (*in_layouts, *(c.format.layout if hasattr(c, 'format')
                                 else None for c in mut.in_mut))
    donated_invars = (*donated_invars,) + (False,) * len(mut.in_mut)
    out_layouts_ = iter(zip(out_shardings, out_layouts))
    out_shardings, out_layouts = unzip2(
        next(out_layouts_) if i is None else (in_shardings[i], in_layouts[i])
        for i in mut.out_mut)
    assert next(out_layouts_, None) is None
  else:
    inout_aliases = mut = None
    if any(isinstance(e, core.InternalMutableArrayEffect) for e in closed_jaxpr.effects):
      closed_jaxpr = _discharge_internal_refs(closed_jaxpr)

  return (closed_jaxpr, inout_aliases, mut, in_shardings, in_layouts,
          donated_invars, out_shardings, out_layouts)

