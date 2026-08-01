
def _fusible_physicalize_rule(
    _, *consts_and_args, jaxpr, num_consts, in_tree, out_tree, func, **params
):
  consts, _ = util.split_list(consts_and_args, [num_consts])
  new_jaxpr = physicalize_closed_jaxpr(core.ClosedJaxpr(jaxpr, consts))
  return fusible_p.bind(
      *consts_and_args,
      jaxpr=new_jaxpr.jaxpr,
      num_consts=num_consts,
      in_tree=in_tree,
      out_tree=out_tree,
      func=func,
      **params,
  )

