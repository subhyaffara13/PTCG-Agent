
def _custom_fusion_impl(
    *args,
    jaxpr: core.Jaxpr,
    num_consts: int,
    pallas_num_consts: int,
    **_):
  consts, _, args = util.split_list(args, [num_consts, pallas_num_consts])
  return core.eval_jaxpr(jaxpr, consts, *args)

