
def _load_pp_rule(eqn, context, settings):
  # Pretty prints `a = load x i` as `x[i] <- a`
  y, = eqn.outvars
  x, transforms, mask, other = tree_util.tree_unflatten(
      eqn.params["args_tree"], eqn.invars
  )
  # TODO(sharadmv): pretty print mask and other
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  lhs = jax_core.pp_vars([y], context, print_shapes=settings.print_shapes,
                         is_binder=True)
  result = [lhs, pp.text(" <- ", annotation=annotation),
            sp.pp_ref_transforms(context, x, transforms)]
  if mask is not None:
    result += [
        pp.text(" "),
        pp.text("mask="),
        jax_core.pp_var(mask, context),
    ]
  if other is not None:
    result += [
        pp.text(" "),
        pp.text("other="),
        jax_core.pp_var(other, context),
    ]
  return pp.concat(result)

