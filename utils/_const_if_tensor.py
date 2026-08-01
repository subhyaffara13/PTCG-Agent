
def _const_if_tensor(graph_context: GraphContext, arg):
    if arg is None:
        return arg
    if isinstance(arg, _C.Value):
        return arg

    return _add_op(graph_context, "onnx::Constant", value_z=arg)

