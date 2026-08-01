
def _while_rule(
    ctx: Context, *args, body_jaxpr, cond_jaxpr, body_nconsts,
    cond_nconsts, **params
):
  _assert_no_fusion_types(ctx.avals_out)
  cond_avals = [v.aval for v in cond_jaxpr.jaxpr.invars]
  _, cond_in_avals = util.split_list(cond_avals, [cond_nconsts])
  _assert_no_fusion_types(cond_in_avals)
  new_cond_jaxpr = physicalize_closed_jaxpr(cond_jaxpr)
  new_num_cond_consts = (
      cond_nconsts
      + len(new_cond_jaxpr.jaxpr.invars)
      - len(cond_jaxpr.jaxpr.invars)
  )

  body_avals = [v.aval for v in body_jaxpr.jaxpr.invars]
  _, body_in_avals = util.split_list(body_avals, [body_nconsts])
  _assert_no_fusion_types(body_in_avals)
  new_body_jaxpr = physicalize_closed_jaxpr(body_jaxpr)
  new_num_body_consts = (
      body_nconsts
      + len(new_body_jaxpr.jaxpr.invars)
      - len(body_jaxpr.jaxpr.invars)
  )
  flat_args = tree_util.tree_leaves(args)
  cond_consts, body_consts, flat_args = util.split_list(
      flat_args, [new_num_cond_consts, new_num_body_consts]
  )
  assert len(flat_args) + len(body_consts) == len(
      new_body_jaxpr.jaxpr.invars), (
      f"Length mismatch: {len(flat_args) + len(body_consts)} !="
      f" {len(new_body_jaxpr.jaxpr.invars)=}"
  )
  assert len(flat_args) + len(cond_consts) == len(
      new_cond_jaxpr.jaxpr.invars), (
      f"Length mismatch: {len(flat_args) + len(cond_consts)} !="
      f" {len(new_cond_jaxpr.jaxpr.invars)=}"
  )
  return jax.lax.while_p.bind(
      *(cond_consts + body_consts + flat_args),
      body_jaxpr=new_body_jaxpr,
      cond_jaxpr=new_cond_jaxpr,
      body_nconsts=new_num_body_consts,
      cond_nconsts=new_num_cond_consts,
      **params,
  )

