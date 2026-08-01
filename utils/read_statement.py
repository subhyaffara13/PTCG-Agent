
def read_statement(state: State, data: ReadBuffer) -> Statement:
    # Branches ordered by frequency (based on mypy self-check)
    tag = read_tag(data)
    stmt: Statement
    if tag == nodes.ASSIGNMENT_STMT:
        lvalues = read_expression_list(state, data)
        rvalue = read_expression(state, data)
        has_type = read_bool(data)
        if has_type:
            type_annotation = read_type(state, data)
        else:
            type_annotation = None
        new_syntax = read_bool(data)
        a = AssignmentStmt(lvalues, rvalue, type=type_annotation, new_syntax=new_syntax)
        read_loc(data, a)
        # If rvalue is TempNode, copy location from AssignmentStmt
        if isinstance(rvalue, TempNode):
            set_line_column_range(rvalue, a)
        expect_end_tag(data)
        return a
    elif tag == nodes.EXPR_STMT:
        es = ExpressionStmt(read_expression(state, data))
        set_line_column_range(es, es.expr)
        expect_end_tag(data)
        return es
    elif tag == nodes.IF_STMT:
        expr = read_expression(state, data)
        body = read_block(state, data)

        num_elif = read_int(data)
        elif_exprs = []
        elif_bodies = []
        for i in range(num_elif):
            elif_exprs.append(read_expression(state, data))
            elif_bodies.append(read_block(state, data))

        has_else = read_bool(data)
        if has_else:
            else_body = read_block(state, data)
        else:
            else_body = None

        # Normalize elif into nested if/else statements
        # Build from the bottom up, starting with the final else body
        current_else = else_body

        for elif_expr, elif_body in reversed(list(zip(elif_exprs, elif_bodies))):
            elif_stmt = IfStmt([elif_expr], [elif_body], current_else)
            elif_stmt.line = elif_expr.line
            elif_stmt.column = elif_expr.column
            if current_else is not None:
                elif_stmt.end_line = current_else.end_line
                elif_stmt.end_column = current_else.end_column
            else:
                elif_stmt.end_line = elif_body.end_line
                elif_stmt.end_column = elif_body.end_column

            current_else = Block([elif_stmt])
            set_line_column_range(current_else, elif_stmt)

        if_stmt = IfStmt([expr], [body], current_else)
        read_loc(data, if_stmt)
        expect_end_tag(data)
        return if_stmt
    elif tag == nodes.RETURN_STMT:
        has_value = read_bool(data)
        if has_value:
            value = read_expression(state, data)
        else:
            value = None
        stmt = ReturnStmt(value)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.FUNC_DEF_STMT:
        return read_func_def(state, data)
    elif tag == nodes.IMPORT_FROM:
        relative = read_int(data)
        module_id = read_str(data)  # Empty string for "from . import x"
        n = read_int(data)
        names = []
        for _ in range(n):
            name = read_str(data)
            has_asname = read_bool(data)
            if has_asname:
                asname = read_str(data)
            else:
                asname = None
            names.append((name, asname))

        stmt = ImportFrom(module_id, relative, names)
        _read_and_set_import_metadata(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.FOR_STMT:
        index = read_expression(state, data)
        expr = read_expression(state, data)
        body = read_block(state, data)
        else_body = read_optional_block(state, data)
        is_async = read_bool(data)
        stmt = ForStmt(index, expr, body, else_body)
        stmt.is_async = is_async
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.ASSERT_STMT:
        test = read_expression(state, data)
        has_msg = read_bool(data)
        if has_msg:
            msg = read_expression(state, data)
        else:
            msg = None
        stmt = AssertStmt(test, msg)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.CLASS_DEF:
        return read_class_def(state, data)
    elif tag == nodes.DECORATOR:
        expect_tag(data, LIST_GEN)
        n_decorators = read_int_bare(data)
        decorators = [read_expression(state, data) for i in range(n_decorators)]
        line = read_int(data)
        column = read_int(data)
        fdef = read_statement(state, data)
        assert isinstance(fdef, FuncDef)
        fdef.is_decorated = True
        var = Var(fdef.name)
        var.line = fdef.line
        var.is_ready = False
        stmt = Decorator(fdef, decorators, var)
        stmt.line = line
        stmt.column = column
        stmt.end_line = fdef.end_line
        stmt.end_column = fdef.end_column
        # TODO: Adjust funcdef location to start after decorator?
        expect_end_tag(data)
        return stmt
    elif tag == nodes.IMPORT:
        n = read_int(data)
        ids = []
        for _ in range(n):
            name = read_str(data)
            has_asname = read_bool(data)
            if has_asname:
                asname = read_str(data)
            else:
                asname = None
            ids.append((name, asname))
        stmt = Import(ids)
        _read_and_set_import_metadata(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.RAISE_STMT:
        has_exc = read_bool(data)
        if has_exc:
            exc = read_expression(state, data)
        else:
            exc = None
        has_from = read_bool(data)
        if has_from:
            from_expr = read_expression(state, data)
        else:
            from_expr = None
        stmt = RaiseStmt(exc, from_expr)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.OPERATOR_ASSIGNMENT_STMT:
        op = read_str(data)
        lvalue = read_expression(state, data)
        rvalue = read_expression(state, data)
        stmt = OperatorAssignmentStmt(op, lvalue, rvalue)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.PASS_STMT:
        stmt = PassStmt()
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.CONTINUE_STMT:
        stmt = ContinueStmt()
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.WITH_STMT:
        n = read_int(data)
        expr_list = []
        target_list: list[Expression | None] = []
        for _ in range(n):
            context_expr = read_expression(state, data)
            expr_list.append(context_expr)
            has_target = read_bool(data)
            if has_target:
                target = read_expression(state, data)
                target_list.append(target)
            else:
                target_list.append(None)
        body = read_block(state, data)
        is_async = read_bool(data)
        stmt = WithStmt(expr_list, target_list, body)
        stmt.is_async = is_async
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.TRY_STMT:
        return read_try_stmt(state, data)
    elif tag == nodes.BREAK_STMT:
        stmt = BreakStmt()
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.WHILE_STMT:
        expr = read_expression(state, data)
        body = read_block(state, data)
        else_body = read_optional_block(state, data)
        stmt = WhileStmt(expr, body, else_body)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.DEL_STMT:
        expr = read_expression(state, data)
        stmt = DelStmt(expr)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.TYPE_ALIAS_STMT:
        return read_type_alias_stmt(state, data)
    elif tag == nodes.IMPORT_ALL:
        module_id = read_str(data)  # Empty string for "from . import *"
        relative = read_int(data)

        stmt = ImportAll(module_id, relative)
        _read_and_set_import_metadata(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.NONLOCAL_DECL:
        n = read_int(data)
        decl_names = []
        for _ in range(n):
            decl_names.append(read_str(data))
        stmt = NonlocalDecl(decl_names)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.GLOBAL_DECL:
        n = read_int(data)
        decl_names = []
        for _ in range(n):
            decl_names.append(read_str(data))
        stmt = GlobalDecl(decl_names)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    elif tag == nodes.MATCH_STMT:
        subject = read_expression(state, data)
        n_cases = read_int(data)
        patterns = []
        guards: list[Expression | None] = []
        bodies = []
        for _ in range(n_cases):
            pattern = read_pattern(state, data)
            patterns.append(pattern)
            has_guard = read_bool(data)
            if has_guard:
                guard = read_expression(state, data)
                guards.append(guard)
            else:
                guards.append(None)
            body = read_block(state, data)
            bodies.append(body)
        stmt = MatchStmt(subject, patterns, guards, bodies)
        read_loc(data, stmt)
        expect_end_tag(data)
        return stmt
    else:
        assert False, tag

