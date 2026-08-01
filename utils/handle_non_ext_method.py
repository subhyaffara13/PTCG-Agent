
def handle_non_ext_method(
    builder: IRBuilder, non_ext: NonExtClassInfo, cdef: ClassDef, fdef: FuncDef
) -> None:
    # Perform the function of visit_method for methods inside non-extension classes.
    name = fdef.name
    sig = builder.mapper.fdef_to_sig(fdef, builder.options.strict_dunders_typing)
    func_ir, func_reg = gen_func_item(builder, fdef, name, sig, cdef)
    assert func_reg is not None
    builder.functions.append(func_ir)

    if is_decorated(builder, fdef):
        # The undecorated method is a generated callable class
        orig_func = func_reg
        func_reg = load_decorated_func(builder, fdef, orig_func)

    # TODO: Support property setters in non-extension classes
    if fdef.is_property:
        prop = builder.load_module_attr_by_fullname("builtins.property", fdef.line)
        func_reg = builder.py_call(prop, [func_reg], fdef.line)

    elif builder.mapper.func_to_decl[fdef].kind == FUNC_CLASSMETHOD:
        cls_meth = builder.load_module_attr_by_fullname("builtins.classmethod", fdef.line)
        func_reg = builder.py_call(cls_meth, [func_reg], fdef.line)

    elif builder.mapper.func_to_decl[fdef].kind == FUNC_STATICMETHOD:
        stat_meth = builder.load_module_attr_by_fullname("builtins.staticmethod", fdef.line)
        func_reg = builder.py_call(stat_meth, [func_reg], fdef.line)

    builder.add_to_non_ext_dict(non_ext, name, func_reg, fdef.line)

    # If we identified that this non-extension class method can be special-cased for
    # direct access during prepare phase, generate a "static" version of it.
    class_ir = builder.mapper.type_to_ir[cdef.info]
    name = FAST_PREFIX + fdef.name
    if name in class_ir.method_decls:
        func_ir, func_reg = gen_func_item(builder, fdef, name, sig, cdef, make_ext_method=True)
        class_ir.methods[name] = func_ir
        builder.functions.append(func_ir)

