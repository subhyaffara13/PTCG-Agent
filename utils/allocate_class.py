
def allocate_class(builder: IRBuilder, cdef: ClassDef) -> Value:
    # OK AND NOW THE FUN PART
    base_exprs = cdef.base_type_exprs + cdef.removed_base_type_exprs
    new_style_type_args = cdef.type_args
    if new_style_type_args:
        bases = [make_generic_base_class(builder, cdef.fullname, new_style_type_args, cdef.line)]
    else:
        bases = []

    if base_exprs or new_style_type_args:
        bases.extend([builder.accept(x) for x in base_exprs])
        tp_bases = builder.new_tuple(bases, cdef.line)
    else:
        tp_bases = builder.add(LoadErrorValue(object_rprimitive, is_borrowed=True))
    modname = builder.load_str(builder.module_name)
    template = builder.add(
        LoadStatic(object_rprimitive, cdef.name + "_template", builder.module_name, NAMESPACE_TYPE)
    )
    # Create the class
    tp = builder.call_c(pytype_from_template_op, [template, tp_bases, modname], cdef.line)

    # Set type object to be immortal if free threaded, as otherwise reference count contention
    # can cause a big performance hit.
    builder.set_immortal_if_free_threaded(tp, cdef.line)

    # Immediately fix up the trait vtables, before doing anything with the class.
    ir = builder.mapper.type_to_ir[cdef.info]
    if not ir.is_trait and not ir.builtin_base:
        builder.add(
            Call(
                FuncDecl(
                    cdef.name + "_trait_vtable_setup",
                    None,
                    builder.module_name,
                    FuncSignature([], bool_rprimitive),
                ),
                [],
                cdef.line,
            )
        )
        builder.add_coroutine_setup_call(cdef.name, tp)

    # Populate a '__mypyc_attrs__' field containing the list of attrs
    builder.primitive_op(
        py_setattr_op,
        [
            tp,
            builder.load_str("__mypyc_attrs__"),
            create_mypyc_attrs_tuple(builder, builder.mapper.type_to_ir[cdef.info], cdef.line),
        ],
        cdef.line,
    )

    # Save the class
    builder.add(InitStatic(tp, cdef.name, builder.module_name, NAMESPACE_TYPE))

    # Add it to the dict
    builder.call_c(
        exact_dict_set_item_op,
        [builder.load_globals_dict(), builder.load_str(cdef.name), tp],
        cdef.line,
    )

    return tp

