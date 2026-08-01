
def make_opaque_bitwise_fn(name, real_op_name):
    if name == "bitwise_and":
        prec = PRECEDENCE["BitwiseAnd"]
    elif name == "bitwise_xor":
        prec = PRECEDENCE["BitwiseXor"]
    elif name == "bitwise_or":
        prec = PRECEDENCE["BitwiseOr"]
    else:
        raise AssertionError(f"unrecognized {name}")

    class BitwiseFn(sympy.Function):
        _torch_handler_name = name
        precedence: int = prec
        _torch_unpickler = functools.partial(
            make_opaque_bitwise_fn, real_op_name=real_op_name
        )

        @classmethod
        def eval(cls, a, b):
            if a.is_Boolean and b.is_Boolean:
                return getattr(operator, real_op_name)(a, b)
            if a.is_Boolean:
                a = sympy.Integer(1 if a else 0)
            if b.is_Boolean:
                b = sympy.Integer(1 if b else 0)
            if isinstance(a, (sympy.Integer, int)) and isinstance(
                b, (sympy.Integer, int)
            ):
                return sympy.Integer(getattr(operator, real_op_name)(int(a), int(b)))
            return None

    nm = "BitwiseFn_" + name
    BitwiseFn.__name__ = nm
    BitwiseFn.__qualname__ = nm

    return BitwiseFn

