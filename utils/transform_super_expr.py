
def transform_super_expr(builder: IRBuilder, o: SuperExpr) -> Value:
    # warning(builder, 'can not optimize super() expression', o.line)
    sup_val = builder.load_module_attr_by_fullname("builtins.super", o.line)
    if o.call.args:
        args = [builder.accept(arg) for arg in o.call.args]
    else:
        assert o.info is not None
        typ = builder.load_native_type_object(o.info.fullname)
        ir = builder.mapper.type_to_ir[o.info]
        iter_env = iter(builder.builder.args)
        # Grab first argument
        vself: Value = next(iter_env)
        if builder.fn_info.is_generator:
            # grab seventh argument (see comment in translate_super_method_call)
            self_targ = list(builder.symtables[-1].values())[7]
            vself = builder.read(self_targ, builder.fn_info.fitem.line)
        elif not ir.is_ext_class:
            vself = next(iter_env)  # second argument is self if non_extension class
        args = [typ, vself]
    res = builder.py_call(sup_val, args, o.line)
    return builder.py_get_attr(res, o.name, o.line)

