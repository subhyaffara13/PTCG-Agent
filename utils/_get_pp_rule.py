
def _get_pp_rule(eqn, context, settings) -> pp.Doc:
  # Pretty prints `a = get x i` as `x[i] <- a`
  y, = eqn.outvars
  x, *flat_idx = eqn.invars
  transforms = tree_util.tree_unflatten(eqn.params["tree"], flat_idx)
  lhs = core.pp_vars([y], context, print_shapes=settings.print_shapes)
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  return pp.concat(
      [lhs, pp.text(" <- ", annotation=annotation),
       pp_ref_transforms(context, x, transforms)]
  )

