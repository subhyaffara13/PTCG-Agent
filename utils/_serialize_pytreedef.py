
def _serialize_pytreedef(
    builder: flatbuffers.Builder, p: tree_util.PyTreeDef
) -> int:
  node_data = p.node_data()
  children = p.children()

  children_vector_offset = None
  children_names_vector_offset = None
  if children:
    children_vector_offset = _serialize_array(
        builder, _serialize_pytreedef, children
    )
  custom_name = None
  custom_auxdata = None
  node_type = node_data and node_data[0]

  if node_data is None:  # leaf
    kind = ser_flatbuf.PyTreeDefKind.leaf
  elif node_type is types.NoneType:
    kind = ser_flatbuf.PyTreeDefKind.none
  elif node_type is tuple:
    kind = ser_flatbuf.PyTreeDefKind.tuple
  elif node_type is list:
    kind = ser_flatbuf.PyTreeDefKind.list
  elif node_type is dict:
    kind = ser_flatbuf.PyTreeDefKind.dict
    assert len(node_data[1]) == len(children)
    def serialize_key(builder, k):
      if not isinstance(k, str):
        raise TypeError(
            "Serialization is supported only for dictionaries with string keys."
            f" Found key {k} of type {type(k)}.")
      return builder.CreateString(k)
    children_names_vector_offset = _serialize_array(
        builder, serialize_key, node_data[1]
    )
  elif node_type in _export.serialization_registry:
    assert node_type is not None
    kind = ser_flatbuf.PyTreeDefKind.custom
    serialized_name, serialize_auxdata = _export.serialization_registry[node_type]
    custom_name = builder.CreateString(serialized_name)
    serialized_auxdata = serialize_auxdata(node_data[1])
    if not isinstance(serialized_auxdata, (bytes, bytearray)):
      raise ValueError(
          "The custom serialization function for `node_type` must "
          f"return a `bytes` object. It returned a {type(serialized_auxdata)}.")
    custom_auxdata = builder.CreateByteVector(serialized_auxdata)
  else:
    raise ValueError(
        "Cannot serialize PyTreeDef containing an "
        f"unregistered type `{node_type}`. "
        "Use `export.register_pytree_node_serialization` or "
        "`export.register_namedtuple_serialization`.")

  ser_flatbuf.PyTreeDefStart(builder)
  ser_flatbuf.PyTreeDefAddKind(builder, kind)
  if children_vector_offset:
    ser_flatbuf.PyTreeDefAddChildren(builder, children_vector_offset)
  if children_names_vector_offset:
    ser_flatbuf.PyTreeDefAddChildrenNames(builder, children_names_vector_offset)
  if custom_name is not None:
    ser_flatbuf.PyTreeDefAddCustomName(builder, custom_name)
  if custom_auxdata is not None:
    ser_flatbuf.PyTreeDefAddCustomAuxdata(builder, custom_auxdata)
  return ser_flatbuf.PyTreeDefEnd(builder)

