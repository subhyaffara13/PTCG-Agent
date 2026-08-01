
def _count_boolean_expressions(bool_op: nodes.BoolOp) -> int:
    """Counts the number of boolean expressions in BoolOp `bool_op` (recursive).

    example: a and (b or c or (d and e)) ==> 5 boolean expressions
    """
    nb_bool_expr = 0
    for bool_expr in bool_op.get_children():
        if isinstance(bool_expr, nodes.BoolOp):
            nb_bool_expr += _count_boolean_expressions(bool_expr)
        else:
            nb_bool_expr += 1
    return nb_bool_expr

