
def merge_operator_dicts(
    lhs: dict[str, SelectiveBuildOperator],
    rhs: dict[str, SelectiveBuildOperator],
) -> dict[str, SelectiveBuildOperator]:
    operators: dict[str, SelectiveBuildOperator] = {}
    for op_name, op in list(lhs.items()) + list(rhs.items()):
        new_op = op
        if op_name in operators:
            new_op = combine_operators(operators[op_name], op)

        operators[op_name] = new_op

    return operators

