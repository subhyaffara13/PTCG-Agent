
def _swap_pp_rule(eqn, context, settings):
  # Pretty prints `a = swap x v i` as `a, x[i] <- x[i], v`
  # or:
  # Pretty prints `_ = swap x v i` as `x[i] <- v`
  y, = eqn.outvars
  x, transforms, val, mask = eqn.params["args_tree"].unflatten(eqn.invars)
  x_i = sp.pp_ref_transforms(context, x, transforms)
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  if isinstance(y, jax_core.DropVar):
    return pp.concat([
        x_i,
        pp.text(" <- ", annotation=annotation),
        jax_core.pp_var(val, context)])
  y = jax_core.pp_vars([y], context, print_shapes=settings.print_shapes,
                       is_binder=True)
  result = [
      y,
      pp.text(", "),
      x_i,
      pp.text(" <- ", annotation=annotation),
      x_i,
      pp.text(", "),
      jax_core.pp_var(val, context),
  ]
  if mask is not None:
    result += [
        pp.text(" "),
        pp.text("mask="),
        jax_core.pp_var(mask, context),
    ]
  return pp.concat(result)


def _swap_pp_rule(eqn, context, settings) -> pp.Doc:
  y, = eqn.outvars
  x, v, *flat_idx = eqn.invars
  transforms = tree_util.tree_unflatten(eqn.params["tree"], flat_idx)
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  if context.var_names.get(y) == '_':
    # In the case of a set (ignored return value), print as `x[i] <- v`
    del y
    return pp.concat([
        pp_ref_transforms(context, x, transforms),
        pp.text(" <- ", annotation=annotation),
        core.pp_var(v, context),
    ])
  else:
    # pretty-print `y:T = swap x v i` as `y:T, x[i] <- x[i], v`
    x_i = pp_ref_transforms(context, x, transforms)
    y = core.pp_vars([y], context, print_shapes=settings.print_shapes)
    return pp.concat([y, pp.text(', '), x_i,
                      pp.text(' <- ', annotation=annotation), x_i,
                      pp.text(', '), core.pp_var(v, context)])

