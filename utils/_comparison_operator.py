
def _comparison_operator(g: jit_utils.GraphContext, input, other, op_name):
    other = symbolic_helper._maybe_get_scalar(other)
    other = symbolic_helper._if_scalar_type_as(other, input)
    _, input, other = _try_cast_integer_to_float(g, input, other)
    return g.op(op_name, input, other)

