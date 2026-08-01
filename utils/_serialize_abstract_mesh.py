
def _serialize_abstract_mesh(builder: flatbuffers.Builder,
                             mesh: mesh.AbstractMesh) -> int:
  ser_flatbuf.AbstractMeshStartAxisSizesVector(builder, len(mesh.axis_sizes))
  for axis_size in reversed(mesh.axis_sizes):
    builder.PrependUint32(axis_size)
  axis_sizes = builder.EndVector()

  axis_names = _serialize_array(builder,
                                lambda builder, an: builder.CreateString(an),
                                mesh.axis_names)

  assert mesh.axis_types is not None, mesh
  ser_flatbuf.AbstractMeshStartAxisTypesVector(builder, len(mesh.axis_types))
  for axis_type in reversed(mesh.axis_types):
    builder.PrependByte(_axis_type_to_enum[axis_type])
  axis_types = builder.EndVector()

  abstract_device = _serialize_abstract_device(builder, mesh.abstract_device)

  ser_flatbuf.AbstractMeshStart(builder)
  ser_flatbuf.AbstractMeshAddAxisSizes(builder, axis_sizes)
  ser_flatbuf.AbstractMeshAddAxisNames(builder, axis_names)
  ser_flatbuf.AbstractMeshAddAxisTypes(builder, axis_types)
  if mesh.abstract_device is not None:
    ser_flatbuf.AbstractMeshAddAbstractDevice(builder, abstract_device)
  return ser_flatbuf.AbstractMeshEnd(builder)

