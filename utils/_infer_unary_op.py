
def _infer_unary_op(obj: Any, op: str) -> ConstFactoryResult:
    """Perform unary operation on `obj`, unless it is `NotImplemented`.

    Can raise TypeError if operation is unsupported.
    """
    if obj is NotImplemented:
        value = obj
    else:
        func = _UNARY_OPERATORS[op]
        value = func(obj)
    return nodes.const_factory(value)

