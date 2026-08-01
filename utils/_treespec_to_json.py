
def _treespec_to_json(treespec: TreeSpec) -> _TreeSpecSchema:
    if treespec.is_leaf():
        return _TreeSpecSchema(None, None, [])

    if treespec.type not in SUPPORTED_SERIALIZED_TYPES:
        raise NotImplementedError(
            f"Serializing {treespec.type} in pytree is not registered.",
        )

    serialize_node_def = SUPPORTED_SERIALIZED_TYPES[treespec.type]

    serialized_type_name = serialize_node_def.serialized_type_name

    if serialized_type_name == NO_SERIALIZED_TYPE_NAME_FOUND:
        raise NotImplementedError(
            f"No registered serialization name for {treespec.type} found. "
            "Please update your _register_pytree_node call with a `serialized_type_name` kwarg."
        )

    if serialize_node_def.to_dumpable_context is None:
        try:
            serialized_context = json.dumps(treespec._context, cls=EnumEncoder)
        except TypeError as e:
            raise TypeError(
                "Unable to serialize context. "
                "Please make the context json dump-able, or register a "
                "custom serializer using _register_pytree_node."
            ) from e
    else:
        serialized_context = serialize_node_def.to_dumpable_context(treespec._context)

    child_schemas = [_treespec_to_json(child) for child in treespec._children]

    return _TreeSpecSchema(serialized_type_name, serialized_context, child_schemas)

