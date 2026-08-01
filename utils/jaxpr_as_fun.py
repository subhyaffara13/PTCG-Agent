
def jaxpr_as_fun(closed_jaxpr: ClosedJaxpr, *args):
  # TODO(dougalm): remove this hack when we add contexts to jaxpr.
  # debug_nans is sometimes disabled locally at the traceable level by ops that
  # work with nans internally, like jnp.var. The right thing to do is to add
  # contexts to our jaxpr representation so that we can capture these local
  # context modifications. In the meantime, disabling the checks when we
  # round-trip prevents those ops producing spurious errors.
  with config.debug_nans(False):
    return eval_jaxpr(closed_jaxpr.jaxpr, closed_jaxpr.consts, *args)

