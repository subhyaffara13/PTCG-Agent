
def not_condition_as_string(
    test_node: nodes.Compare | nodes.Name | nodes.UnaryOp | nodes.BoolOp | nodes.BinOp,
) -> str:
    match test_node:
        case nodes.UnaryOp():
            return test_node.operand.as_string()  # type: ignore[no-any-return]
        case nodes.BoolOp():
            return f"not ({test_node.as_string()})"
        case nodes.Compare():
            lhs = test_node.left
            ops, rhs = test_node.ops[0]
            lower_priority_expressions = (
                nodes.Lambda,
                nodes.UnaryOp,
                nodes.BoolOp,
                nodes.IfExp,
                nodes.NamedExpr,
            )
            lhs = (
                f"({lhs.as_string()})"
                if isinstance(lhs, lower_priority_expressions)
                else lhs.as_string()
            )
            rhs = (
                f"({rhs.as_string()})"
                if isinstance(rhs, lower_priority_expressions)
                else rhs.as_string()
            )
            return f"{lhs} {get_inverse_comparator(ops)} {rhs}"
        case _:
            return f"not {test_node.as_string()}"

