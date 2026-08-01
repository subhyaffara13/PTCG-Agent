
def generate_clear_for_class(cl: ClassIR, func_name: str, emitter: Emitter) -> None:
    emitter.emit_line("static int")
    emitter.emit_line(f"{func_name}({cl.struct_name(emitter.names)} *self)")
    emitter.emit_line("{")
    for base in reversed(cl.base_mro):
        for attr, rtype in base.attributes.items():
            emitter.emit_gc_clear(f"self->{emitter.attr(attr)}", rtype)
    base_args = "(PyObject *)self"
    if cl.builtin_base:
        emitter.emit_base_tp_function_call(cl, "tp_clear", base_args)
    if has_managed_dict(cl, emitter):
        emitter.emit_line(f"PyObject_ClearManagedDict({base_args});")
    elif cl.has_dict:
        struct_name = cl.struct_name(emitter.names)
        # __dict__ lives right after the struct and __weakref__ lives right after that
        emitter.emit_gc_clear(
            f"*((PyObject **)((char *)self + sizeof({struct_name})))", object_rprimitive
        )
        emitter.emit_gc_clear(
            f"*((PyObject **)((char *)self + sizeof(PyObject *) + sizeof({struct_name})))",
            object_rprimitive,
        )
    emitter.emit_line("return 0;")
    emitter.emit_line("}")

