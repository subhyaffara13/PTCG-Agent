
def register_constant(cls: type[Any]) -> None:
    """Registers a type as a pytree node with no leaves.

    In a :func:`torch.compile` region, if instances of these types get passed to
    :func:`torch._dynamo.nonstrict_trace`-ed function, they treated as a
    constant (sometimes referred to as "static"):

    1. if the instance object existed before the :func:`torch.compile` region,
    we _assume_ no mutation will happen to it inside the :func:`torch.compile`
    region, require that it has non-default `__eq__` and `__hash__` methods, and
    we guard on the instance based on its `__eq__` method, i.e., if a new
    instance fails to match any instances from the previous compilations,
    :func:`torch.compile` will recompile the function using the new instance.

    2. else if the instance object is created inside the :func:`torch.compile`
    region, we currently don't support using it in a
    :func:`torch._dynamo.nonstrict_trace`-ed function.

    In general, if your class holds Tensors or dynamic int/float/bool (values that
    may change from run-to-run of a function being compiled), then you probably
    do not want to register it as a constant.

    Otherwise if you want to pass instance of a class to a
    :func:`torch._dynamo.nonstrict_trace`-ed function, but you either can't use
    :func:`register_pytree_node` on the class, or the class is "constant" enough
    that you don't want to bother using :func:`register_pytree_node`, you should
    consider using this function.

    Args:
        cls: the type to register as a constant. This type must be hashable.

    Example:

        >>> from dataclasses import dataclass
        >>> import torch.utils._pytree as pytree
        >>>
        >>> @dataclass(frozen=True)
        >>> class Config:
        >>>     norm: str
        >>>
        >>> pytree.register_constant(Config)
        >>>
        >>> config = Config("l2")
        >>> values, spec = pytree.tree_flatten(config)
        >>> assert len(values) == 0

    """
    if cls.__eq__ is object.__eq__:  # type: ignore[comparison-overlap]
        raise TypeError(
            "register_constant(cls) expects `cls` to have a non-default `__eq__` implementation."
        )

    # Class with a custom `__eq__` without `__hash__` won't inherit the default
    # `__hash__` from object; see https://stackoverflow.com/a/1608907.
    if cls.__hash__ is None:  # type: ignore[comparison-overlap]
        raise TypeError(
            "register_constant(cls) expects `cls` to have a non-default `__hash__` implementation."
        )

    def _flatten(x):  # type: ignore[no-untyped-def]
        return [], ConstantNode(x)

    def _unflatten(_, context):  # type: ignore[no-untyped-def]
        return context.value

    def _flatten_with_keys(x):  # type: ignore[no-untyped-def]
        return [], ConstantNode(x)

    with _NODE_REGISTRY_LOCK:
        _private_register_pytree_node(
            cls,
            _flatten,
            _unflatten,
            flatten_with_keys_fn=_flatten_with_keys,
        )
        CONSTANT_NODES.add(cls)

