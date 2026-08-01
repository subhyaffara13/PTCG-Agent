
def transform_comparison_expr(builder: IRBuilder, e: ComparisonExpr) -> Value:
    # x in (...)/[...]
    # x not in (...)/[...]
    first_op = e.operators[0]
    if first_op in ["in", "not in"] and len(e.operators) == 1:
        result = try_specialize_in_expr(builder, first_op, e.operands[0], e.operands[1], e.line)
        if result is not None:
            return result

    if len(e.operators) == 1:
        # s[i] == 'x' / s[i] != 'x' (and the symmetric RHS) -> int compare of
        # codepoints. Skips the per-iteration 1-char str allocation/lookup and
        # generic str equality call.
        if first_op in ("==", "!="):
            result = try_specialize_str_index_compare(
                builder, first_op, e.operands[0], e.operands[1], e.line
            )
            if result is not None:
                return result

        # Special some common simple cases
        if first_op in ("is", "is not"):
            right_expr = e.operands[1]
            if isinstance(right_expr, NameExpr) and right_expr.fullname == "builtins.None":
                # Special case 'is None' / 'is not None'.
                return translate_is_none(builder, e.operands[0], negated=first_op != "is")
        left_expr = e.operands[0]
        if is_int_rprimitive(builder.node_type(left_expr)):
            right_expr = e.operands[1]
            if is_int_rprimitive(builder.node_type(right_expr)):
                if first_op in int_borrow_friendly_op:
                    borrow_left = is_borrow_friendly_expr(builder, right_expr)
                    left = builder.accept(left_expr, can_borrow=borrow_left)
                    right = builder.accept(right_expr, can_borrow=True)
                    return builder.binary_op(left, right, first_op, e.line)

    # TODO: Don't produce an expression when used in conditional context
    # All of the trickiness here is due to support for chained conditionals
    # (`e1 < e2 > e3`, etc). `e1 < e2 > e3` is approximately equivalent to
    # `e1 < e2 and e2 > e3` except that `e2` is only evaluated once.
    expr_type = builder.node_type(e)

    # go(i, prev) generates code for `ei opi e{i+1} op{i+1} ... en`,
    # assuming that prev contains the value of `ei`.
    def go(i: int, prev: Value) -> Value:
        if i == len(e.operators) - 1:
            return transform_basic_comparison(
                builder, e.operators[i], prev, builder.accept(e.operands[i + 1]), e.line
            )

        next = builder.accept(e.operands[i + 1])
        return builder.builder.shortcircuit_helper(
            "and",
            expr_type,
            lambda: transform_basic_comparison(builder, e.operators[i], prev, next, e.line),
            lambda: go(i + 1, next),
            e.line,
        )

    return go(0, builder.accept(e.operands[0]))

