
def translate_super_method_call(builder: IRBuilder, expr: CallExpr, callee: SuperExpr) -> Value:
    if callee.info is None or (len(callee.call.args) != 0 and len(callee.call.args) != 2):
        return translate_call(builder, expr, callee)

    # We support two-argument super but only when it is super(CurrentClass, self)
    # TODO: We could support it when it is a parent class in many cases?
    if len(callee.call.args) == 2:
        self_arg = callee.call.args[1]
        if (
            not isinstance(self_arg, NameExpr)
            or not isinstance(self_arg.node, Var)
            or not self_arg.node.is_self
        ):
            return translate_call(builder, expr, callee)

        typ_arg = callee.call.args[0]
        if (
            not isinstance(typ_arg, NameExpr)
            or not isinstance(typ_arg.node, TypeInfo)
            or callee.info is not typ_arg.node
        ):
            return translate_call(builder, expr, callee)

    ir = builder.mapper.type_to_ir[callee.info]
    # Search for the method in the mro, skipping ourselves. We
    # determine targets of super calls to native methods statically.
    for base in ir.mro[1:]:
        if callee.name in base.method_decls:
            break
    else:
        if callee.name == "__new__":
            result = translate_object_new(builder, expr, MemberExpr(callee.call, "__new__"))
            if result:
                return result
        elif callee.name == "__setattr__":
            result = translate_object_setattr(
                builder, expr, MemberExpr(callee.call, "__setattr__")
            )
            if result:
                return result
        if ir.is_ext_class and ir.builtin_base is None and not ir.inherits_python:
            if callee.name == "__init__" and len(expr.args) == 0:
                # Call translates to object.__init__(self), which is a
                # no-op, so omit the call.
                return builder.none()
        return translate_call(builder, expr, callee)

    decl = base.method_decl(callee.name)
    arg_values = [builder.accept(arg) for arg in expr.args]
    arg_kinds, arg_names = expr.arg_kinds.copy(), expr.arg_names.copy()

    if decl.kind != FUNC_STATICMETHOD and decl.name != "__new__":
        # Grab first argument
        vself: Value = builder.self()
        if decl.kind == FUNC_CLASSMETHOD:
            vself = builder.primitive_op(type_op, [vself], expr.line)
        elif builder.fn_info.is_generator:
            # For generator classes, the self target is the 7th value
            # in the symbol table (which is an ordered dict). This is sort
            # of ugly, but we can't search by name since the 'self' parameter
            # could be named anything, and it doesn't get added to the
            # environment indexes.
            self_targ = list(builder.symtables[-1].values())[7]
            vself = builder.read(self_targ, builder.fn_info.fitem.line)
        arg_values.insert(0, vself)
        arg_kinds.insert(0, ARG_POS)
        arg_names.insert(0, None)

    return builder.builder.call(decl, arg_values, arg_kinds, arg_names, expr.line)

