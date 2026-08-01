
def _is_constant(node):
    return isinstance(node, ast.Constant) or _is_tuple_constant(node)


def _is_constant(val: _ExprType):
    if isinstance(val, sympy.Basic):
        return val.is_number
    return isinstance(val, (int, float, bool))


def _is_constant(value: Any) -> bool:
    return not _is_value(value) or value.node().kind() in {
        "onnx::Constant",
        "prim::Constant",
    }

