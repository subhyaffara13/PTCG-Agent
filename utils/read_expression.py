
def read_expression(state: State, data: ReadBuffer) -> Expression:
    # Branches ordered by frequency (based on mypy self-check)
    tag = read_tag(data)
    expr: Expression
    if tag == nodes.NAME_EXPR:
        s = read_str(data)
        ne = NameExpr(s)
        read_loc(data, ne)
        expect_end_tag(data)
        return ne
    elif tag == nodes.MEMBER_EXPR:
        e = read_expression(state, data)
        attr = read_str(data)
        m = MemberExpr(e, attr)
        # Check if this is a super() call - if so, convert to SuperExpr
        if isinstance(e, CallExpr) and isinstance(e.callee, NameExpr) and e.callee.name == "super":
            result: Expression = SuperExpr(attr, e)
        else:
            result = m
        read_loc(data, result)
        expect_end_tag(data)
        return result
    elif tag == nodes.CALL_EXPR:
        callee = read_expression(state, data)
        args = read_expression_list(state, data)
        # Read argument kinds
        expect_tag(data, LIST_INT)
        n_kinds = read_int_bare(data)
        arg_kinds = [ARG_KINDS[read_int_bare(data)] for _ in range(n_kinds)]
        # Read argument names
        expect_tag(data, LIST_GEN)
        n_names = read_int_bare(data)
        arg_names: list[str | None] = []
        for _ in range(n_names):
            tag = read_tag(data)
            if tag == LITERAL_NONE:
                arg_names.append(None)
            elif tag == LITERAL_STR:
                arg_names.append(read_str_bare(data))
            else:
                assert False, f"Unexpected tag for arg_name: {tag}"
        ce = CallExpr(callee, args, arg_kinds, arg_names)
        read_loc(data, ce)
        expect_end_tag(data)
        return ce
    elif tag == nodes.STR_EXPR:
        se = StrExpr(read_str(data))
        read_loc(data, se)
        expect_end_tag(data)
        return se
    elif tag == nodes.COMPARISON_EXPR:
        left = read_expression(state, data)
        expect_tag(data, LIST_INT)
        n_ops = read_int_bare(data)
        ops = [cmp_ops[read_int_bare(data)] for _ in range(n_ops)]
        comparators = read_expression_list(state, data)
        assert len(ops) == len(comparators)
        expr = ComparisonExpr(ops, [left] + comparators)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.INT_EXPR:
        ie = IntExpr(read_int(data))
        read_loc(data, ie)
        expect_end_tag(data)
        return ie
    elif tag == nodes.INDEX_EXPR:
        base = read_expression(state, data)
        index = read_expression(state, data)
        expr = IndexExpr(base, index)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.LIST_EXPR:
        items = read_expression_list(state, data)
        expr = ListExpr(items)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.TUPLE_EXPR:
        items = read_expression_list(state, data)
        t = TupleExpr(items)
        read_loc(data, t)
        expect_end_tag(data)
        return t
    elif tag == nodes.BOOL_OP_EXPR:
        op = bool_ops[read_int(data)]
        values = read_expression_list(state, data)
        # Convert list of values to nested OpExpr nodes
        # E.g., [a, b, c] with "and" becomes OpExpr("and", a, OpExpr("and", b, c))
        # This matches the old parser behavior, on which we may implicitly rely.
        assert len(values) >= 2
        result = last = values[-1]
        for val in values[-2::-1]:
            result = OpExpr(op, val, result)
            result.line = val.line
            result.column = val.column
            result.end_line = last.end_line
            result.end_column = last.end_column
        read_loc(data, result)
        expect_end_tag(data)
        return result
    elif tag == nodes.UNARY_EXPR:
        op = unary_ops[read_int(data)]
        operand = read_expression(state, data)
        expr = UnaryExpr(op, operand)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.OP_EXPR:
        op = bin_ops[read_int(data)]
        left = read_expression(state, data)
        right = read_expression(state, data)
        o = OpExpr(op, left, right)
        # TODO: Store these explicitly?
        o.line = left.line
        o.column = left.column
        o.end_line = right.end_line
        o.end_column = right.end_column
        expect_end_tag(data)
        return o
    elif tag == nodes.FSTRING_EXPR:
        # F-strings are converted into nodes representing "".join([...]), to match
        # pre-existing behavior.
        nparts = read_int(data)
        fitems = []
        for _ in range(nparts):
            b = read_bool(data)
            if b:
                n = read_int(data)
                for i in range(n):
                    fitems.append(read_fstring_item(state, data))
            else:
                s = StrExpr(read_str(data))
                read_loc(data, s)
                fitems.append(s)
        expr = build_fstring_join(data, fitems)
        expect_end_tag(data)
        return expr
    elif tag == nodes.LIST_COMPREHENSION:
        generator = read_generator_expr(state, data)
        expr = ListComprehension(generator)
        read_loc(data, expr)
        set_line_column_range(generator, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.DICT_EXPR:
        expect_tag(data, LIST_GEN)
        n_keys = read_int_bare(data)
        keys: list[Expression | None] = []
        for _ in range(n_keys):
            has_key = read_bool(data)
            if has_key:
                keys.append(read_expression(state, data))
            else:
                keys.append(None)
        values = read_expression_list(state, data)
        items = list(zip(keys, values))
        expr = DictExpr(items)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.TEMP_NODE:
        temp = TempNode(AnyType(TypeOfAny.special_form), no_rhs=True)
        expect_end_tag(data)
        return temp
    elif tag == nodes.CONDITIONAL_EXPR:
        if_expr = read_expression(state, data)
        cond = read_expression(state, data)
        else_expr = read_expression(state, data)
        expr = ConditionalExpr(cond, if_expr, else_expr)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.SLICE_EXPR:
        has_begin = read_bool(data)
        begin_index = read_expression(state, data) if has_begin else None
        has_end = read_bool(data)
        end_index = read_expression(state, data) if has_end else None
        has_stride = read_bool(data)
        stride = read_expression(state, data) if has_stride else None
        expr = SliceExpr(begin_index, end_index, stride)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.GENERATOR_EXPR:
        expr = read_generator_expr(state, data)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.YIELD_EXPR:
        has_value = read_bool(data)
        if has_value:
            value = read_expression(state, data)
        else:
            value = None
        expr = YieldExpr(value)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.SET_EXPR:
        items = read_expression_list(state, data)
        expr = SetExpr(items)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.ELLIPSIS_EXPR:
        expr = EllipsisExpr()
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.TSTRING_EXPR:
        nparts = read_int(data)
        titems: list[Expression | tuple[Expression, str, str | None, Expression | None]] = []
        for _ in range(nparts):
            if read_bool(data):
                e = read_expression(state, data)
                s = read_str(data)
                if read_bool(data):
                    conv = read_str(data)
                else:
                    conv = None
                if read_bool(data):
                    # Parse format spec as a JoinedStr, this matches the old parser behavior.
                    format_spec = read_fstring_items(state, data)
                else:
                    format_spec = None
                titems.append((e, s, conv, format_spec))
            else:
                s = StrExpr(read_str(data))
                read_loc(data, s)
                titems.append(s)
        expr = TemplateStrExpr(titems)
        read_loc(data, expr)
        state.check_min_version(
            "t-strings", (3, 14), expr.line, expr.column, enforce_in_stubs=True
        )
        expect_end_tag(data)
        return expr
    elif tag == nodes.LAMBDA_EXPR:
        arguments, has_ann = read_parameters(state, data)
        body = read_block(state, data)

        if has_ann:
            typ = CallableType(
                [
                    arg.type_annotation if arg.type_annotation else AnyType(TypeOfAny.unannotated)
                    for arg in arguments
                ],
                [arg.kind for arg in arguments],
                [None if arg.pos_only else arg.variable.name for arg in arguments],
                AnyType(TypeOfAny.unannotated),
                _dummy_fallback,
            )
        else:
            typ = None

        expr = LambdaExpr(arguments, body)
        expr.type = typ
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.DICT_COMPREHENSION:
        key = read_expression(state, data)
        value = read_expression(state, data)
        n_generators = read_int(data)
        indices = [read_expression(state, data) for _ in range(n_generators)]
        sequences = [read_expression(state, data) for _ in range(n_generators)]
        condlists = [read_expression_list(state, data) for _ in range(n_generators)]
        is_async = [read_bool(data) for _ in range(n_generators)]
        expr = DictionaryComprehension(key, value, indices, sequences, condlists, is_async)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.SET_COMPREHENSION:
        generator = read_generator_expr(state, data)
        expr = SetComprehension(generator)
        read_loc(data, expr)
        set_line_column_range(generator, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.BYTES_EXPR:
        value = read_str(data)
        expr = BytesExpr(value)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.ASSIGNMENT_EXPR:
        target = read_expression(state, data)
        value = read_expression(state, data)
        assert isinstance(target, NameExpr), f"Expected NameExpr for target, got {type(target)}"
        expr = AssignmentExpr(target, value)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.FLOAT_EXPR:
        expect_tag(data, LITERAL_FLOAT)
        value = read_float_bare(data)
        fe = FloatExpr(value)
        read_loc(data, fe)
        expect_end_tag(data)
        return fe
    elif tag == nodes.STAR_EXPR:
        wrapped_expr = read_expression(state, data)
        expr = StarExpr(wrapped_expr)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.YIELD_FROM_EXPR:
        value = read_expression(state, data)
        expr = YieldFromExpr(value)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.AWAIT_EXPR:
        value = read_expression(state, data)
        expr = AwaitExpr(value)
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.COMPLEX_EXPR:
        expect_tag(data, LITERAL_FLOAT)
        real = read_float_bare(data)
        expect_tag(data, LITERAL_FLOAT)
        imag = read_float_bare(data)
        expr = ComplexExpr(complex(real, imag))
        read_loc(data, expr)
        expect_end_tag(data)
        return expr
    elif tag == nodes.BIG_INT_EXPR:
        strval = read_str(data)
        ie = IntExpr(int(strval, base=0))
        read_loc(data, ie)
        expect_end_tag(data)
        return ie
    else:
        assert False, tag

