from typing import Optional

def _get_sym_val(node: fx.Node) -> Optional["sympy.Expr"]:
    val = _get_example_value(node)
    if isinstance(val, py_sym_types):
        return val.node.expr
    return None

