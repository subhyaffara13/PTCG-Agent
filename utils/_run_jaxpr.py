
def _run_jaxpr(jaxpr, consts, *args):
  def _run(jaxpr, consts, *args):
    jax_core.eval_jaxpr(jaxpr, consts, *args)

  traced = jax.jit(_run, static_argnums=(0,)).trace(jaxpr, consts, *args)
  traced.lower().compile()(consts, *args)
  return

