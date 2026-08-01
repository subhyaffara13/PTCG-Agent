
def _deserialize_pytreedef_to_pytree(
    p: ser_flatbuf.PyTreeDef,
    leaf_iterator: Iterator[Any],
) -> tree_util.PyTree:
  """Deserializes a PyTreeDef into a PyTree using an iterator over leaves."""
  kind = p.Kind()
  nr_children = p.ChildrenLength()
  children = [
      _deserialize_pytreedef_to_pytree(p.Children(i), leaf_iterator)
      for i in range(nr_children)
  ]
  if kind == ser_flatbuf.PyTreeDefKind.leaf:
    return next(leaf_iterator)
  elif kind == ser_flatbuf.PyTreeDefKind.none:
    return None
  elif kind == ser_flatbuf.PyTreeDefKind.tuple:
    return tuple(children)
  elif kind == ser_flatbuf.PyTreeDefKind.list:
    return list(children)
  elif kind == ser_flatbuf.PyTreeDefKind.dict:
    assert p.ChildrenNamesLength() == nr_children
    keys = [p.ChildrenNames(i).decode("utf-8") for i in range(nr_children)]
    return dict(zip(keys, children))
  elif kind == ser_flatbuf.PyTreeDefKind.custom:
    serialized_name = p.CustomName().decode("utf-8")
    if serialized_name not in _export.deserialization_registry:
      raise ValueError(
          "Cannot deserialize a PyTreeDef containing an "
          f"unregistered type `{serialized_name}`. "
          "Use `export.register_pytree_node_serialization` or "
          "`export.register_namedtuple_serialization`.")
    nodetype, deserialize_auxdata, from_iter = _export.deserialization_registry[serialized_name]
    auxdata = deserialize_auxdata(p.CustomAuxdataAsNumpy().tobytes())
    return from_iter(auxdata, children)
  else:
    raise ValueError(
        f"Cannot deserialize PyTreeDef with unknown kind: {kind}")

