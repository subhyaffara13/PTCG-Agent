
def translate_method_call(builder: IRBuilder, expr: CallExpr, callee: MemberExpr) -> Value:
    """Generate IR for an arbitrary call of form e.m(...).

    This can also deal with calls to module-level functions.
    """
    if builder.is_native_ref_expr(callee):
        # Call to module-level native function or such
        return translate_call(builder, expr, callee)
    elif (
        isinstance(callee.expr, RefExpr)
        and isinstance(callee.expr.node, TypeInfo)
        and callee.expr.node in builder.mapper.type_to_ir
        and builder.mapper.type_to_ir[callee.expr.node].has_method(callee.name)
        and all(kind in (ARG_POS, ARG_NAMED) for kind in expr.arg_kinds)
    ):
        # Call a method via the *class*
        assert isinstance(callee.expr.node, TypeInfo), callee.expr.node
        ir = builder.mapper.type_to_ir[callee.expr.node]
        return call_classmethod(builder, ir, expr, callee)
    elif builder.is_module_member_expr(callee):
        # Fall back to a PyCall for non-native module calls
        function = builder.accept(callee)
        args = [builder.accept(arg) for arg in expr.args]
        return builder.py_call(
            function, args, expr.line, arg_kinds=expr.arg_kinds, arg_names=expr.arg_names
        )
    else:
        if isinstance(callee.expr, RefExpr):
            node = callee.expr.node
            if isinstance(node, Var) and node.is_cls:
                typ = get_proper_type(node.type)
                if isinstance(typ, TypeType) and isinstance(typ.item, Instance):
                    class_ir = builder.mapper.type_to_ir.get(typ.item.type)
                    if class_ir and class_ir.is_ext_class and class_ir.has_no_subclasses():
                        # Call a native classmethod via cls that can be statically bound,
                        # since the class has no subclasses.
                        return call_classmethod(builder, class_ir, expr, callee)

        receiver_typ = builder.node_type(callee.expr)

        # If there is a specializer for this method name/type, try calling it.
        # We would return the first successful one.
        val = apply_method_specialization(builder, expr, callee, receiver_typ)
        if val is not None:
            return val

        obj = builder.accept(callee.expr)
        args = [builder.accept(arg) for arg in expr.args]
        return builder.gen_method_call(
            obj,
            callee.name,
            args,
            builder.node_type(expr),
            expr.line,
            expr.arg_kinds,
            expr.arg_names,
        )

