
def _serialize_named_sharding(
    builder: flatbuffers.Builder, sharding: named_sharding.NamedSharding, *,
    uniques: _SerializedUniques
) -> int:
  abstract_mesh_idx = uniques.abstract_meshes_map[sharding.mesh.abstract_mesh]
  # TODO(necula): 1 month after 4/4/26 we can stop serializing the full
  # abstract_mesh and only serialize the index.
  mesh_offset = _serialize_abstract_mesh(builder, sharding.mesh.abstract_mesh)
  spec_offset = _serialize_partition_spec(builder, sharding.spec)
  memory_kind = builder.CreateString(sharding.memory_kind) if sharding.memory_kind is not None else 0

  ser_flatbuf.NamedShardingStart(builder)
  ser_flatbuf.NamedShardingAddMesh(builder, mesh_offset)
  ser_flatbuf.NamedShardingAddSpec(builder, spec_offset)
  if memory_kind != 0:
    ser_flatbuf.NamedShardingAddMemoryKind(builder, memory_kind)
  ser_flatbuf.NamedShardingAddAbstractMeshIdx(builder, abstract_mesh_idx)
  return ser_flatbuf.NamedShardingEnd(builder)

