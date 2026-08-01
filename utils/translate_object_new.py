
def translate_object_new(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    fn = builder.fn_info
    if fn.name != "__new__" or not is_super_or_object(expr, callee):
        return None

    ir = builder.get_current_class_ir()
    if ir is None:
        return None

    call = '"object.__new__()"'
    if not ir.is_ext_class:
        builder.error(f"{call} not supported for non-extension classes", expr.line)
        return None
    if ir.inherits_python:
        builder.error(
            f"{call} not supported for classes inheriting from non-native classes", expr.line
        )
        return None
    if len(expr.args) != 1:
        builder.error(f"{call} supported only with 1 argument, got {len(expr.args)}", expr.line)
        return None

    typ_arg = expr.args[0]
    method_args = fn.fitem.arg_names
    if isinstance(typ_arg, NameExpr) and len(method_args) > 0 and method_args[0] == typ_arg.name:
        subtype = builder.accept(expr.args[0])
        subs = ir.subclasses()
        if subs is not None and len(subs) == 0:
            return builder.add(Call(ir.setup, [subtype], expr.line))
        # Call a function that dynamically resolves the setup function of extension classes from the type object.
        # This is necessary because the setup involves default attribute initialization and setting up
        # the vtable which are specific to a given type and will not work if a subtype is created using
        # the setup function of its base.
        return builder.call_c(setup_object, [subtype], expr.line)

    return None

