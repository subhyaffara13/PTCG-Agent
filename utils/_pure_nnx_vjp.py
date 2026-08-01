
def _pure_nnx_vjp(f, model, *args, **kwargs):
  "Wrap nnx functional api around jax.vjp. Only handles pure method calls."
  graphdef, state = nnx.split(model)
  def inner(state, *args, **kwargs):
    model = nnx.merge(graphdef, state)
    return f(model, *args, **kwargs)
  return jax.vjp(inner, state, *args, **kwargs)

