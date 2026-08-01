
def _addupdate_pp_rule(eqn, context, settings) -> pp.Doc:
  # pretty-print ` = addupdate x i v` as `x[i] += v`
  () = eqn.outvars
  x, v, *flat_idx = eqn.invars
  transforms = tree_util.tree_unflatten(eqn.params["tree"], flat_idx)
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  return pp.concat([
      pp_ref_transforms(context, x, transforms),
      pp.text(" += ", annotation=annotation),
      core.pp_var(v, context),
  ])

