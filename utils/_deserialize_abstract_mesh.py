
def _deserialize_abstract_mesh(
  ser_mesh: ser_flatbuf.AbstractMesh) -> mesh.AbstractMesh:
  axis_sizes = tuple(ser_mesh.AxisSizes(i)
                     for i in range(ser_mesh.AxisSizesLength()))
  axis_names = tuple(ser_mesh.AxisNames(i).decode("utf-8")
                     for i in range(ser_mesh.AxisNamesLength()))
  axis_types = tuple(_axis_type_from_enum[ser_mesh.AxisTypes(i)]
                     for i in range(ser_mesh.AxisTypesLength()))
  abstract_device = _deserialize_abstract_device(ser_mesh.AbstractDevice())
  return mesh.AbstractMesh(axis_sizes, axis_names, axis_types,
                           abstract_device=abstract_device)

