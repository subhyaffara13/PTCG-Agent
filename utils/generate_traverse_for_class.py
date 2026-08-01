
def generate_traverse_for_class(cl: ClassIR, func_name: str, emitter: Emitter) -> None:
    """Emit function that performs cycle GC traversal of an instance."""
    emitter.emit_line("static int")
    emitter.emit_line(
        f"{func_name}({cl.struct_name(emitter.names)} *self, visitproc visit, void *arg)"
    )
    emitter.emit_line("{")
    for base in reversed(cl.base_mro):
        for attr, rtype in base.attributes.items():
            emitter.emit_gc_visit(f"self->{emitter.attr(attr)}", rtype)
    base_args = "(PyObject *)self, visit, arg"
    emitter.emit_line("int rv = 0;")
    if cl.builtin_base:
        emitter.emit_base_tp_function_call(cl, "tp_traverse", base_args, prefix="rv = ")
        emitter.emit_line("if (rv != 0) return rv;")
    if has_managed_dict(cl, emitter):
        emitter.emit_line(f"rv = PyObject_VisitManagedDict({base_args});")
        emitter.emit_line("if (rv != 0) return rv;")
    elif cl.has_dict:
        struct_name = cl.struct_name(emitter.names)
        # __dict__ lives right after the struct and __weakref__ lives right after that
        emitter.emit_gc_visit(
            f"*((PyObject **)((char *)self + sizeof({struct_name})))", object_rprimitive
        )
        emitter.emit_gc_visit(
            f"*((PyObject **)((char *)self + sizeof(PyObject *) + sizeof({struct_name})))",
            object_rprimitive,
        )
    emitter.emit_line("return rv;")
    emitter.emit_line("}")

