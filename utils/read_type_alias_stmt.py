
def read_type_alias_stmt(state: State, data: ReadBuffer) -> TypeAliasStmt:
    """Read PEP 695 type alias statement."""
    name = read_expression(state, data)
    assert isinstance(name, NameExpr), f"Expected NameExpr for type alias name, got {type(name)}"

    n_type_params = read_int_bare(data)
    if n_type_params > 0:
        type_params = []
        for _ in range(n_type_params):
            kind = read_int(data)
            param_name = read_str(data)
            has_bound = read_bool(data)
            if has_bound:
                upper_bound = read_type(state, data)
            else:
                upper_bound = None

            # Read values (for constrained TypeVar)
            expect_tag(data, LIST_GEN)
            n_values = read_int_bare(data)
            values = [read_type(state, data) for _ in range(n_values)]

            has_default = read_bool(data)
            if has_default:
                default = read_type(state, data)
            else:
                default = None

            type_params.append(TypeParam(param_name, kind, upper_bound, values, default))
    else:
        type_params = []

    value_expr = read_expression(state, data)

    # Wrap the value expression in a LambdaExpr as expected by TypeAliasStmt
    # The LambdaExpr body is a Block with a single ReturnStmt
    return_stmt = ReturnStmt(value_expr)
    set_line_column_range(return_stmt, value_expr)

    block = Block([return_stmt])
    block.line = -1  # Synthetic block
    block.column = 0
    block.end_line = -1
    block.end_column = 0

    lambda_expr = LambdaExpr([], block)
    set_line_column_range(lambda_expr, value_expr)

    stmt = TypeAliasStmt(name, type_params, lambda_expr)
    read_loc(data, stmt)
    state.check_min_version('"type" statements', (3, 12), stmt.line, stmt.column)
    check_type_param_defaults(state, type_params, stmt.line, stmt.column)
    expect_end_tag(data)
    return stmt

