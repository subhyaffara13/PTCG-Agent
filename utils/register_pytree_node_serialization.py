
def register_pytree_node_serialization(
    nodetype: type[T],
    *,
    serialized_name: str,
    serialize_auxdata: _SerializeAuxData,
    deserialize_auxdata: _DeserializeAuxData,
    from_children: _BuildFromChildren | None = None
) -> type[T]:
  """Registers a custom PyTree node for serialization and deserialization.

  You must use this function before you can serialize and deserialize PyTree
  nodes for the types not supported natively. We serialize PyTree nodes for
  the ``in_tree`` and ``out_tree`` fields of ``Exported``, which are part of the
  exported function's calling convention.

  This function must be called after calling
  :func:`jax.tree_util.register_pytree_node` (except for ``collections.namedtuple``,
  which do not require a call to ``register_pytree_node``).

  Args:
    nodetype: the type whose PyTree nodes we want to serialize. It is an
      error to attempt to register multiple serializations for a ``nodetype``.
    serialized_name: a string that will be present in the serialization and
      will be used to look up the registration during deserialization. It is an
      error to attempt to register multiple serializations for a
      ``serialized_name``.
    serialize_auxdata: serialize the PyTree auxdata (returned by the
      ``flatten_func`` argument to :func:`jax.tree_util.register_pytree_node`.).
    deserialize_auxdata: deserialize the auxdata that was serialized by the
      ``serialize_auxdata``.
    from_children: if present, this is a function that takes that result of
      ``deserialize_auxdata`` along with some children and creates an instance
      of ``nodetype``. This is similar to the ``unflatten_func`` passed to
      :func:`jax.tree_util.register_pytree_node`. If not present, we look up
      and use the ``unflatten_func``. This is needed for ``collections.namedtuple``,
      which does not have a ``register_pytree_node``, but it can be useful to
      override that function. Note that the result of ``from_children`` is
      only used with :func:`jax.tree_util.tree_structure` to construct a proper
      PyTree node, it is not used to construct the outputs of the serialized
      function.

  Returns:
    the same type passed as ``nodetype``, so that this function can
    be used as a class decorator.
  """
  if nodetype in serialization_registry:
    raise ValueError(
        f"Duplicate serialization registration for type `{nodetype}`. "
        "Previous registration was with serialized_name "
        f"`{serialization_registry[nodetype][0]}`.")
  if serialized_name in deserialization_registry:
    raise ValueError(
        "Duplicate serialization registration for "
        f"serialized_name `{serialized_name}`. "
        "Previous registration was for type "
        f"`{deserialization_registry[serialized_name][0]}`.")
  if from_children is None:
    if nodetype not in tree_util._registry:
      raise ValueError(
          f"If `from_children` is not present, you must call first"
          f"`jax.tree_util.register_pytree_node` for `{nodetype}`")
    from_children = tree_util._registry[nodetype].from_iter

  serialization_registry[nodetype] = (
      serialized_name, serialize_auxdata)
  deserialization_registry[serialized_name] = (
      nodetype, deserialize_auxdata, from_children)
  return nodetype

