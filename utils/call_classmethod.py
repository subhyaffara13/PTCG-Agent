
def call_classmethod(builder: IRBuilder, ir: ClassIR, expr: CallExpr, callee: MemberExpr) -> Value:
    decl = ir.method_decl(callee.name)
    args = []
    arg_kinds, arg_names = expr.arg_kinds.copy(), expr.arg_names.copy()
    # Add the class argument for class methods in extension classes
    if decl.kind == FUNC_CLASSMETHOD and ir.is_ext_class:
        args.append(builder.load_native_type_object(ir.fullname))
        arg_kinds.insert(0, ARG_POS)
        arg_names.insert(0, None)
    args += [builder.accept(arg) for arg in expr.args]

    if ir.is_ext_class:
        return builder.builder.call(decl, args, arg_kinds, arg_names, expr.line)
    else:
        obj = builder.accept(callee.expr)
        return builder.gen_method_call(
            obj,
            callee.name,
            args,
            builder.node_type(expr),
            expr.line,
            expr.arg_kinds,
            expr.arg_names,
        )

