
def transform_assignment_stmt(builder: IRBuilder, stmt: AssignmentStmt) -> None:
    lvalues = stmt.lvalues
    assert lvalues
    builder.disallow_class_assignments(lvalues, stmt.line)
    check_unsupported_cls_assignment(builder, stmt)
    first_lvalue = lvalues[0]
    if stmt.type and isinstance(stmt.rvalue, TempNode):
        # This is actually a variable annotation without initializer. Don't generate
        # an assignment but we need to call get_assignment_target since it adds a
        # name binding as a side effect.
        builder.get_assignment_target(first_lvalue, stmt.line)
        return

    # Special case multiple assignments like 'x, y = e1, e2'.
    if (
        isinstance(first_lvalue, (TupleExpr, ListExpr))
        and isinstance(stmt.rvalue, (TupleExpr, ListExpr))
        and len(first_lvalue.items) == len(stmt.rvalue.items)
        and all(is_simple_lvalue(item) for item in first_lvalue.items)
        and len(lvalues) == 1
    ):
        temps = []
        for right in stmt.rvalue.items:
            rvalue_reg = builder.accept(right)
            temp = Register(rvalue_reg.type)
            builder.assign(temp, rvalue_reg, stmt.line)
            temps.append(temp)
        for left, temp in zip(first_lvalue.items, temps):
            assignment_target = builder.get_assignment_target(left)
            builder.assign(assignment_target, temp, stmt.line)
        builder.flush_keep_alives(stmt.line)
        return

    line = stmt.rvalue.line
    rvalue_reg = builder.accept(stmt.rvalue)

    if builder.non_function_scope() and stmt.is_final_def:
        builder.init_final_static(first_lvalue, rvalue_reg)

    # Special-case multiple assignments like 'x, y = expr' to reduce refcount ops.
    if (
        isinstance(first_lvalue, (TupleExpr, ListExpr))
        and isinstance(rvalue_reg.type, RTuple)
        and len(rvalue_reg.type.types) == len(first_lvalue.items)
        and len(lvalues) == 1
        and all(is_simple_lvalue(item) for item in first_lvalue.items)
        and any(t.is_refcounted for t in rvalue_reg.type.types)
    ):
        n = len(first_lvalue.items)
        borrows = [builder.add(TupleGet(rvalue_reg, i, borrow=True)) for i in range(n)]
        builder.builder.keep_alive([rvalue_reg], line, steal=True)
        for lvalue_item, rvalue_item in zip(first_lvalue.items, borrows):
            rvalue_item = builder.add(Unborrow(rvalue_item))
            builder.assign(builder.get_assignment_target(lvalue_item), rvalue_item, line)
        builder.flush_keep_alives(line)
        return

    for lvalue in lvalues:
        # Check for __setitem__ dunder specialization before converting to assignment target
        if isinstance(lvalue, IndexExpr):
            specialized = apply_dunder_specialization(
                builder, lvalue.base, [lvalue.index, stmt.rvalue], "__setitem__", lvalue
            )
            if specialized is not None:
                builder.flush_keep_alives(lvalue.line)
                continue

        target = builder.get_assignment_target(lvalue)
        builder.assign(target, rvalue_reg, line)
        builder.flush_keep_alives(line)

