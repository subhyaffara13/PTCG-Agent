
def _private_register_pytree_node(
    cls: type[Any],
    flatten_fn: FlattenFn,
    unflatten_fn: UnflattenFn,
    *,
    serialized_type_name: str | None = None,
    to_dumpable_context: ToDumpableContextFn | None = None,
    from_dumpable_context: FromDumpableContextFn | None = None,
) -> None:
    """This is an internal function that is used to register a pytree node type
    for the C++ pytree only. End-users should use :func:`register_pytree_node`
    instead.
    """
    # TODO(XuehaiPan): remove this condition when we make Python pytree out-of-box support
    # PyStructSequence types
    if not optree.is_structseq_class(cls):
        optree.register_pytree_node(
            cls,
            flatten_fn,
            _reverse_args(unflatten_fn),
            namespace="torch",
        )


def _private_register_pytree_node(
    cls: type[Any],
    flatten_fn: FlattenFn,
    unflatten_fn: UnflattenFn,
    *,
    serialized_type_name: str | None = None,
    to_dumpable_context: ToDumpableContextFn | None = None,
    from_dumpable_context: FromDumpableContextFn | None = None,
    flatten_with_keys_fn: FlattenWithKeysFn | None = None,
) -> None:
    """This is an internal function that is used to register a pytree node type
    for the Python pytree only. End-users should use :func:`register_pytree_node`
    instead.
    """
    from torch._library.opaque_object import is_opaque_type

    if isinstance(cls, type) and is_opaque_type(cls):
        # TODO: remove this allowance once downstream callers stop calling
        # register_constant on Enum subclasses. Enums are now natively
        # supported as opaque value types and don't need pytree registration.
        import enum

        if issubclass(cls, enum.Enum):
            log.warning(
                "%s is an Enum subclass and is now natively supported by "
                "torch.compile as an opaque value type. Calling "
                "register_constant() on Enum subclasses is deprecated and "
                "will be an error in a future release.",
                cls,
            )
        else:
            raise ValueError(
                f"{cls} cannot be registered as a pytree as it has been "
                "registered as an opaque object. Opaque objects must be pytree leaves."
            )

    with _NODE_REGISTRY_LOCK:
        if cls in SUPPORTED_NODES:
            # TODO: change this warning to an error after OSS/internal stabilize
            warnings.warn(
                f"{cls} is already registered as pytree node. "
                "Overwriting the previous registration.",
                stacklevel=2,
            )

        node_def = NodeDef(cls, flatten_fn, unflatten_fn, flatten_with_keys_fn)
        SUPPORTED_NODES[cls] = node_def

        if (to_dumpable_context is None) ^ (from_dumpable_context is None):
            raise ValueError(
                f"Both to_dumpable_context and from_dumpable_context for {cls} must "
                "be None or registered."
            )

        if serialized_type_name is None:
            serialized_type_name = NO_SERIALIZED_TYPE_NAME_FOUND

        serialize_node_def = _SerializeNodeDef(
            cls,
            serialized_type_name,
            to_dumpable_context,
            from_dumpable_context,
        )
        SUPPORTED_SERIALIZED_TYPES[cls] = serialize_node_def
        SERIALIZED_TYPE_TO_PYTHON_TYPE[serialized_type_name] = cls

