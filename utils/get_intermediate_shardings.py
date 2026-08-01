
def get_intermediate_shardings(
    jaxpr: core.Jaxpr) -> Sequence[tuple[Sharding, SourceInfo]]:
  from jax._src import shard_map  # pyrefly: ignore[missing-module-attribute]

  out = []
  for eqn in jaxpr.eqns:
    if eqn.primitive is pjit.sharding_constraint_p:
      s = eqn.params['sharding']
      if isinstance(s, NamedSharding) and isinstance(s.mesh, AbstractMesh):
        continue
      source_info = SourceInfo(eqn.source_info, eqn.primitive.name)
      out.append((s, source_info))
    elif eqn.primitive is pjit.jit_p:
      source_info = SourceInfo(eqn.source_info, eqn.primitive.name)
      out.extend((i, source_info) for i in eqn.params['in_shardings'])
      out.extend((o, source_info) for o in eqn.params['out_shardings'])
    elif eqn.primitive is shard_map.shard_map_p:
      mesh = eqn.params['mesh']
      if isinstance(mesh, AbstractMesh):
        continue
      source_info = SourceInfo(eqn.source_info, eqn.primitive.name)
      out.extend((NamedSharding(mesh, spec), source_info)
                 for spec in [*eqn.params['in_specs'], *eqn.params['out_specs']])
    elif eqn.primitive is device_put_p:
      source_info = SourceInfo(eqn.source_info, eqn.primitive.name)
      out.extend((s, source_info) for s in eqn.params['devices']
                 if isinstance(s, Sharding) and s.memory_kind is not None)
  for subjaxpr in core.subjaxprs(jaxpr):
    out.extend(get_intermediate_shardings(subjaxpr))
  return out

