
def try_specialize_in_expr(
    builder: IRBuilder, op: str, lhs: Expression, rhs: Expression, line: int
) -> Value | None:
    left: Value | None = None
    items: list[Value] | None = None

    if isinstance(rhs, (TupleExpr, ListExpr)):
        left = builder.accept(lhs)
        items = [builder.accept(item) for item in rhs.items]
    elif isinstance(builder.node_type(rhs), RTuple):
        left = builder.accept(lhs)
        tuple_val = builder.accept(rhs)
        assert isinstance(tuple_val.type, RTuple)
        items = [builder.add(TupleGet(tuple_val, i)) for i in range(len(tuple_val.type.types))]

    if items is not None:
        assert left is not None
        n_items = len(items)
        # x in y -> x == y[0] or ... or x == y[n]
        # x not in y -> x != y[0] and ... and x != y[n]
        if n_items > 1:
            if op == "in":
                cmp_op = "=="
            else:
                cmp_op = "!="
            out = BasicBlock()
            for item in items:
                cmp = transform_basic_comparison(builder, cmp_op, left, item, line)
                bool_val = builder.builder.bool_value(cmp)
                next_block = BasicBlock()
                if op == "in":
                    builder.add_bool_branch(bool_val, out, next_block)
                else:
                    builder.add_bool_branch(bool_val, next_block, out)
                builder.activate_block(next_block)
            result_reg = Register(bool_rprimitive)
            end = BasicBlock()
            if op == "in":
                values = builder.false(), builder.true()
            else:
                values = builder.true(), builder.false()
            builder.assign(result_reg, values[0], line)
            builder.goto(end)
            builder.activate_block(out)
            builder.assign(result_reg, values[1], line)
            builder.goto(end)
            builder.activate_block(end)
            return result_reg
        # x in [y]/(y) -> x == y
        # x not in [y]/(y) -> x != y
        elif n_items == 1:
            if op == "in":
                cmp_op = "=="
            else:
                cmp_op = "!="
            right = items[0]
            return transform_basic_comparison(builder, cmp_op, left, right, line)
        # x in []/() -> False
        # x not in []/() -> True
        elif n_items == 0:
            if op == "in":
                return builder.false()
            else:
                return builder.true()

    # x in {...}
    # x not in {...}
    if isinstance(rhs, SetExpr):
        set_literal = precompute_set_literal(builder, rhs)
        if set_literal is not None:
            result = builder.builder.primitive_op(
                set_in_op, [builder.accept(lhs), set_literal], line, bool_rprimitive
            )
            if op == "not in":
                return builder.unary_op(result, "not", line)
            return result

    return None

