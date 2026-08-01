
def _eval_jaxpr_ad_error(dis_jaxpr, consts, args):
  return core.eval_jaxpr(dis_jaxpr, consts, *args)

