
def cached_named_sharding(
    mesh: Mesh | AbstractMesh, pspec: PartitionSpec,
    memory_kind: str | None = None) -> NamedSharding:
  return NamedSharding(mesh, pspec, memory_kind=memory_kind)

