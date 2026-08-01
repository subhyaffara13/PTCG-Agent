
def get_abstract_model(init_fn, mesh, *, graph: bool | None = None):
  with jax.set_mesh(mesh):
    abs_model = eval_shape(init_fn, graph=graph)
    gdef, abs_state = graphlib.split(abs_model, graph=graph)
    abs_state = jax.tree.map(
      lambda a, s: jax.ShapeDtypeStruct(a.shape, a.dtype, sharding=s),
      abs_state, get_named_sharding(abs_state, mesh)
    )
  return gdef, abs_state

