
def wrap_logical_op_with_cast_to(to_type):
    def decorator(fn):
        @functools.wraps(fn)
        def wrap_with_cast(g, input, other):
            to_i = symbolic_helper.cast_pytorch_to_onnx[to_type]
            return fn(g, g.op("Cast", input, to_i=to_i), g.op("Cast", other, to_i=to_i))

        return wrap_with_cast

    return decorator

