
def translate_isinstance(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    """Special case for builtins.isinstance.

    Prevent coercions on the thing we are checking the instance of -
    there is no need to coerce something to a new type before checking
    what type it is, and the coercion could lead to bugs.
    """
    if not (len(expr.args) == 2 and expr.arg_kinds == [ARG_POS, ARG_POS]):
        return None

    obj_expr = expr.args[0]
    type_expr = expr.args[1]

    if isinstance(type_expr, TupleExpr) and not type_expr.items:
        # we can compile this case to a noop
        return builder.false()

    if isinstance(type_expr, (RefExpr, TupleExpr)):
        builder.types[obj_expr] = AnyType(TypeOfAny.from_error)

        irs = builder.flatten_classes(type_expr)
        if irs is not None:
            can_borrow = all(
                ir.is_ext_class and not ir.inherits_python and not ir.allow_interpreted_subclasses
                for ir in irs
            )
            obj = builder.accept(obj_expr, can_borrow=can_borrow)
            return builder.builder.isinstance_helper(obj, irs, expr.line)

    if isinstance(type_expr, RefExpr):
        node = type_expr.node
        if node:
            desc = isinstance_primitives.get(node.fullname)
            if desc:
                obj = builder.accept(obj_expr)
                return builder.primitive_op(desc, [obj], expr.line)

    elif isinstance(type_expr, TupleExpr):
        node_names: list[str] = []
        for item in type_expr.items:
            if not isinstance(item, RefExpr):
                return None
            if item.node is None:
                return None
            if item.node.fullname not in node_names:
                node_names.append(item.node.fullname)

        descs = [isinstance_primitives.get(fullname) for fullname in node_names]
        if None in descs:
            # not all types are primitive types, abort
            return None

        obj = builder.accept(obj_expr)

        retval = Register(bool_rprimitive)
        pass_block = BasicBlock()
        fail_block = BasicBlock()
        exit_block = BasicBlock()

        # Chain the checks: if any succeed, jump to pass_block; else, continue
        for i, desc in enumerate(descs):
            is_last = i == len(descs) - 1
            next_block = fail_block if is_last else BasicBlock()
            builder.add_bool_branch(
                builder.primitive_op(cast(PrimitiveDescription, desc), [obj], expr.line),
                pass_block,
                next_block,
            )
            if not is_last:
                builder.activate_block(next_block)

        # If any check passed
        builder.activate_block(pass_block)
        builder.assign(retval, builder.true(), expr.line)
        builder.goto(exit_block)

        # If all checks failed
        builder.activate_block(fail_block)
        builder.assign(retval, builder.false(), expr.line)
        builder.goto(exit_block)

        # Return the result
        builder.activate_block(exit_block)
        return retval

    return None

