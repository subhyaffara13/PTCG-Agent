
def _deserialize_named_sharding(
    s: ser_flatbuf.NamedSharding, *, uniques: _SerializedUniques
) -> named_sharding.NamedSharding:
  if uniques.unique_abstract_meshes:
    amesh = uniques.unique_abstract_meshes[s.AbstractMeshIdx()]
  else:
    # TODO(necula): 6 months after 4/4/26 we can stop deserializing the full
    # abstract_mesh.
    amesh = _deserialize_abstract_mesh(s.Mesh())
  spec = _deserialize_partition_spec(s.Spec())
  memory_kind = s.MemoryKind().decode("utf-8") if s.MemoryKind() is not None else None
  return named_sharding.NamedSharding(amesh, spec, memory_kind=memory_kind)

