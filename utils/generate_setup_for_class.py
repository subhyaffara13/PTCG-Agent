
def generate_setup_for_class(
    cl: ClassIR,
    defaults_fn: FuncIR | None,
    vtable_name: str,
    shadow_vtable_name: str | None,
    emitter: Emitter,
) -> None:
    """Generate a native function that allocates an instance of a class."""
    emitter.emit_line(native_function_header(cl.setup, emitter))
    emitter.emit_line("{")
    type_arg_name = REG_PREFIX + cl.setup.sig.args[0].name
    emitter.emit_line(f"PyTypeObject *type = (PyTypeObject*){type_arg_name};")
    struct_name = cl.struct_name(emitter.names)
    emitter.emit_line(f"{struct_name} *self;")

    prefix = cl.name_prefix(emitter.names)
    if cl.reuse_freed_instance:
        # Attempt to use a per-type free list first (a free "list" with up to one object only).
        emitter.emit_line(f"if ({prefix}_free_instance != NULL) {{")
        emitter.emit_line(f"self = {prefix}_free_instance;")
        emitter.emit_line(f"{prefix}_free_instance = NULL;")
        emitter.emit_line("Py_SET_REFCNT(self, 1);")
        if not cl.is_acyclic:
            emitter.emit_line("PyObject_GC_Track(self);")
        if defaults_fn is not None:
            emit_attr_defaults_func_call(defaults_fn, "self", emitter)
        emitter.emit_line("return (PyObject *)self;")
        emitter.emit_line("}")

    emitter.emit_line(f"self = ({cl.struct_name(emitter.names)} *)type->tp_alloc(type, 0);")
    emitter.emit_line("if (self == NULL)")
    emitter.emit_line("    return NULL;")

    if shadow_vtable_name:
        emitter.emit_line(f"if (type != {emitter.type_struct_name(cl)}) {{")
        emitter.emit_line(f"self->vtable = {shadow_vtable_name};")
        emitter.emit_line("} else {")
        emitter.emit_line(f"self->vtable = {vtable_name};")
        emitter.emit_line("}")
    else:
        emitter.emit_line(f"self->vtable = {vtable_name};")

    emit_clear_bitmaps(cl, emitter)

    if cl.has_method("__call__"):
        name = cl.method_decl("__call__").cname(emitter.names)
        emitter.emit_line(f"self->vectorcall = {PREFIX}{name};")

    for base in reversed(cl.base_mro):
        for attr, rtype in base.attributes.items():
            value = emitter.c_undefined_value(rtype)

            # We don't need to set this field to NULL since tp_alloc() already
            # zero-initializes `self`.
            if value != "NULL":
                emitter.set_undefined_value(f"self->{emitter.attr(attr)}", rtype)

    # Initialize attributes to default values, if necessary
    if defaults_fn is not None:
        emit_attr_defaults_func_call(defaults_fn, "self", emitter)

    emitter.emit_line("return (PyObject *)self;")
    emitter.emit_line("}")

