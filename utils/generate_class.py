
def generate_class(cl: ClassIR, module: str, emitter: Emitter) -> None:
    """Generate C code for a class.

    This is the main entry point to the module.
    """
    name = cl.name
    name_prefix = cl.name_prefix(emitter.names)

    setup_name = emitter.native_function_name(cl.setup)
    new_name = f"{name_prefix}_new"
    finalize_name = f"{name_prefix}_finalize"
    members_name = f"{name_prefix}_members"
    getseters_name = f"{name_prefix}_getseters"
    vtable_name = f"{name_prefix}_vtable"
    traverse_name = f"{name_prefix}_traverse"
    clear_name = f"{name_prefix}_clear"
    dealloc_name = f"{name_prefix}_dealloc"
    methods_name = f"{name_prefix}_methods"
    vtable_setup_name = f"{name_prefix}_trait_vtable_setup"
    coroutine_setup_name = f"{name_prefix}_coroutine_setup"

    fields: dict[str, str] = {"tp_name": f'"{name}"'}

    generate_full = not cl.is_trait and not cl.builtin_base
    needs_getseters = cl.needs_getseters or not cl.is_generated or cl.has_dict

    if not cl.builtin_base:
        fields["tp_new"] = new_name

    managed_dict = has_managed_dict(cl, emitter)
    if generate_full or managed_dict:
        fields["tp_dealloc"] = f"(destructor){name_prefix}_dealloc"
        if not cl.is_acyclic:
            fields["tp_traverse"] = f"(traverseproc){name_prefix}_traverse"
            fields["tp_clear"] = f"(inquiry){name_prefix}_clear"
    # Populate .tp_finalize and generate a finalize method only if __del__ is defined for this class.
    del_method = next((e.method for e in cl.vtable_entries if e.name == "__del__"), None)
    if del_method:
        fields["tp_finalize"] = f"(destructor){finalize_name}"
    if needs_getseters:
        fields["tp_getset"] = getseters_name
    fields["tp_methods"] = methods_name

    def emit_line() -> None:
        emitter.emit_line()

    emit_line()

    # If the class has a method to initialize default attribute
    # values, we need to call it during initialization.
    defaults_fn = cl.get_method(MYPYC_DEFAULTS_SETUP)

    # If there is a __init__ method, we'll use it in the native constructor.
    init_fn = cl.get_method("__init__")

    # Fill out slots in the type object from dunder methods.
    fields.update(generate_slots(cl, SLOT_DEFS, emitter))

    # Fill out dunder methods that live in tables hanging off the side.
    for table_name, type, slot_defs in SIDE_TABLES:
        slots = generate_slots(cl, slot_defs, emitter)
        if slots:
            table_struct_name = generate_side_table_for_class(cl, table_name, type, slots, emitter)
            fields[f"tp_{table_name}"] = f"&{table_struct_name}"

    richcompare_name = generate_richcompare_wrapper(cl, emitter)
    if richcompare_name:
        fields["tp_richcompare"] = richcompare_name

    # If the class inherits from python, make space for a __dict__
    struct_name = cl.struct_name(emitter.names)
    if cl.builtin_base:
        base_size = f"sizeof({cl.builtin_base})"
    elif cl.is_trait:
        base_size = "sizeof(PyObject)"
    else:
        base_size = f"sizeof({struct_name})"
    # Since our types aren't allocated using type() we need to
    # populate these fields ourselves if we want them to have correct
    # values. PyType_Ready will inherit the offsets from tp_base but
    # that isn't what we want.

    # XXX: there is no reason for the __weakref__ stuff to be mixed up with __dict__
    if cl.has_dict and not has_managed_dict(cl, emitter):
        # __dict__ lives right after the struct and __weakref__ lives right after that
        # TODO: They should get members in the struct instead of doing this nonsense.
        weak_offset = f"{base_size} + sizeof(PyObject *)"
        emitter.emit_lines(
            f"PyMemberDef {members_name}[] = {{",
            f'{{"__dict__", T_OBJECT_EX, {base_size}, 0, NULL}},',
            f'{{"__weakref__", T_OBJECT_EX, {weak_offset}, 0, NULL}},',
            "{0}",
            "};",
        )

        fields["tp_members"] = members_name
        fields["tp_basicsize"] = f"{base_size} + 2*sizeof(PyObject *)"
        if emitter.capi_version < (3, 12):
            fields["tp_dictoffset"] = base_size
            fields["tp_weaklistoffset"] = weak_offset
    else:
        fields["tp_basicsize"] = base_size

    if generate_full or managed_dict:
        if not cl.is_acyclic:
            generate_traverse_for_class(cl, traverse_name, emitter)
            emit_line()
        generate_clear_for_class(cl, clear_name, emitter)
        emit_line()
        generate_dealloc_for_class(cl, dealloc_name, clear_name, bool(del_method), emitter)
        emit_line()
    if generate_full:
        assert cl.setup is not None
        emitter.emit_line(native_function_header(cl.setup, emitter) + ";")
        assert cl.ctor is not None
        emitter.emit_line(native_function_header(cl.ctor, emitter) + ";")

        emit_line()
        init_fn = cl.get_method("__init__")
        generate_new_for_class(cl, new_name, vtable_name, setup_name, init_fn, emitter)
        emit_line()

        if cl.allow_interpreted_subclasses:
            shadow_vtable_name: str | None = generate_vtables(
                cl, vtable_setup_name + "_shadow", vtable_name + "_shadow", emitter, shadow=True
            )
            emit_line()
        else:
            shadow_vtable_name = None
        vtable_name = generate_vtables(cl, vtable_setup_name, vtable_name, emitter, shadow=False)
        emit_line()
        generate_coroutine_setup(cl, coroutine_setup_name, module, emitter)
        emit_line()
    if del_method:
        generate_finalize_for_class(del_method, finalize_name, emitter)
        emit_line()
    if needs_getseters:
        generate_getseter_declarations(cl, emitter)
        emit_line()
        generate_getseters_table(cl, getseters_name, emitter)
        emit_line()

    if cl.is_trait:
        generate_new_for_trait(cl, new_name, emitter)

    generate_methods_table(cl, methods_name, setup_name if generate_full else None, emitter)
    emit_line()

    flags = ["Py_TPFLAGS_DEFAULT", "Py_TPFLAGS_HEAPTYPE", "Py_TPFLAGS_BASETYPE"]
    if (generate_full or managed_dict) and not cl.is_acyclic:
        flags.append("Py_TPFLAGS_HAVE_GC")
    if cl.has_method("__call__"):
        fields["tp_vectorcall_offset"] = "offsetof({}, vectorcall)".format(
            cl.struct_name(emitter.names)
        )
        flags.append("_Py_TPFLAGS_HAVE_VECTORCALL")
        if not fields.get("tp_vectorcall"):
            # This is just a placeholder to please CPython. It will be
            # overridden during setup.
            fields["tp_call"] = "PyVectorcall_Call"
    if managed_dict:
        flags.append("Py_TPFLAGS_MANAGED_DICT")
    fields["tp_flags"] = " | ".join(flags)

    fields["tp_doc"] = f"PyDoc_STR({native_class_doc_initializer(cl)})"

    emitter.emit_line(f"static PyTypeObject {emitter.type_struct_name(cl)}_template_ = {{")
    emitter.emit_line("PyVarObject_HEAD_INIT(NULL, 0)")
    for field, value in fields.items():
        emitter.emit_line(f".{field} = {value},")
    emitter.emit_line("};")
    emitter.emit_line(
        "static PyTypeObject *{t}_template = &{t}_template_;".format(
            t=emitter.type_struct_name(cl)
        )
    )

    if cl.coroutine_name:
        cpyfunction = emitter.static_name(cl.name + "_cpyfunction", module)
        emitter.emit_line(f"static PyObject *{cpyfunction} = NULL;")

    emitter.emit_line()
    if generate_full:
        generate_setup_for_class(cl, defaults_fn, vtable_name, shadow_vtable_name, emitter)
        emitter.emit_line()
        generate_constructor_for_class(cl, cl.ctor, init_fn, setup_name, vtable_name, emitter)
        emitter.emit_line()
    if needs_getseters:
        generate_getseters(cl, emitter)

