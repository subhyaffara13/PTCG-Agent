
def _sharding_constraint_abstract_eval(
    x_aval, *, sharding, layout, context_mesh, unconstrained_dims):
  if isinstance(sharding, NamedSharding):
    return x_aval.update(
        sharding=x_aval.sharding.update(mesh=sharding.mesh.abstract_mesh))
  return x_aval.update(sharding=None)

