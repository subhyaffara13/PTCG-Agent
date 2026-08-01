
def _core_map_typecheck_rule(_, *in_atoms, jaxpr, mesh, **kwargs):
  with jax_core.extend_axis_env_nd(tuple(mesh.shape.items())), config._check_vma(False):
    jax_core.check_jaxpr(jaxpr)
  return _core_map_abstract_eval(*in_atoms, jaxpr=jaxpr, mesh=mesh, **kwargs)

