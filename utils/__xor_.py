
def __xor_(g: jit_utils.GraphContext, input, other):
    if not symbolic_helper._is_bool(input):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise XOR "
            "for non-boolean input values",
            input,
        )
    if not symbolic_helper._is_bool(other):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise XOR "
            "for non-boolean input values",
            other,
        )
    return g.op("Xor", input, other)

