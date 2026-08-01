
def _looks_like_special_alias(node: nodes.Call) -> bool:
    """Return True if call is for Tuple or Callable alias.

    In PY37 and PY38 the call is to '_VariadicGenericAlias' with 'tuple' as
    first argument. In PY39+ it is replaced by a call to '_TupleType'.

    PY37: Tuple = _VariadicGenericAlias(tuple, (), inst=False, special=True)
    PY39: Tuple = _TupleType(tuple, -1, inst=False, name='Tuple')

    PY37: Callable = _VariadicGenericAlias(collections.abc.Callable, (), special=True)
    PY39: Callable = _CallableType(collections.abc.Callable, 2)
    """
    return (
        isinstance(node.func, nodes.Name)
        and node.args
        and (
            (
                node.func.name == "_TupleType"
                and isinstance(node.args[0], nodes.Name)
                and node.args[0].name == "tuple"
            )
            or (
                node.func.name == "_CallableType"
                and isinstance(node.args[0], nodes.Attribute)
                and node.args[0].as_string() == "collections.abc.Callable"
            )
        )
    )

