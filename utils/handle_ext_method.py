
def handle_ext_method(builder: IRBuilder, cdef: ClassDef, fdef: FuncDef) -> None:
    # Perform the function of visit_method for methods inside extension classes.
    name = fdef.name
    class_ir = builder.mapper.type_to_ir[cdef.info]
    sig = builder.mapper.fdef_to_sig(fdef, builder.options.strict_dunders_typing)
    func_ir, func_reg = gen_func_item(builder, fdef, name, sig, cdef)
    builder.functions.append(func_ir)

    if is_decorated(builder, fdef):
        # Obtain the function name in order to construct the name of the helper function.
        _, _, name = fdef.fullname.rpartition(".")
        # Read the PyTypeObject representing the class, get the callable object
        # representing the non-decorated method
        typ = builder.load_native_type_object(cdef.fullname)
        orig_func = builder.py_get_attr(typ, name, fdef.line)

        # Decorate the non-decorated method
        decorated_func = load_decorated_func(builder, fdef, orig_func)

        # Set the callable object representing the decorated method as an attribute of the
        # extension class.
        builder.primitive_op(
            py_setattr_op, [typ, builder.load_str(name), decorated_func], fdef.line
        )

    if fdef.is_property:
        # If there is a property setter, it will be processed after the getter,
        # We populate the optional setter field with none for now.
        assert name not in class_ir.properties
        class_ir.properties[name] = (func_ir, None)

    elif fdef in builder.prop_setters:
        # The respective property getter must have been processed already
        assert name in class_ir.properties
        getter_ir, _ = class_ir.properties[name]
        class_ir.properties[name] = (getter_ir, func_ir)

    class_ir.methods[func_ir.decl.name] = func_ir

    # If this overrides a parent class method with a different type, we need
    # to generate a glue method to mediate between them.
    for base in class_ir.mro[1:]:
        if (
            name in base.method_decls
            and name != "__init__"
            and not is_same_method_signature(
                class_ir.method_decls[name].sig, base.method_decls[name].sig
            )
        ):
            # TODO: Support contravariant subtyping in the input argument for
            # property setters. Need to make a special glue method for handling this,
            # similar to gen_glue_property.

            f = gen_glue(builder, base.method_decls[name].sig, func_ir, class_ir, base, fdef)
            class_ir.glue_methods[(base, name)] = f
            builder.functions.append(f)

    # If the class allows interpreted children, create glue
    # methods that dispatch via the Python API. These will go in a
    # "shadow vtable" that will be assigned to interpreted
    # children.
    if class_ir.allow_interpreted_subclasses:
        f = gen_glue(builder, func_ir.sig, func_ir, class_ir, class_ir, fdef, do_py_ops=True)
        # Use func_ir.decl.name (unique) rather than fdef.name, because for properties
        # the getter and setter share the same fdef.name but have distinct decl names
        # (e.g. "prop" vs "__mypyc_setter__prop"). Using fdef.name would cause the
        # setter's glue to overwrite the getter's glue in the shadow vtable.
        class_ir.glue_methods[(class_ir, func_ir.decl.name)] = f
        builder.functions.append(f)

    if fdef.name == "__getattr__":
        generate_getattr_wrapper(builder, cdef, fdef)
    elif fdef.name == "__setattr__":
        generate_setattr_wrapper(builder, cdef, fdef)
    elif fdef.name == "__delattr__":
        setattr = cdef.info.get("__setattr__")
        if not setattr or not setattr.node or setattr.node.fullname.startswith("builtins."):
            builder.error(
                '"__delattr__" supported only in classes that also override "__setattr__", '
                + "or inherit from a native class that overrides it.",
                fdef.line,
            )

