
def generate_class_reuse(
    cl: ClassIR, c_emitter: Emitter, external_emitter: Emitter, emitter: Emitter
) -> None:
    """Generate a definition of a single-object per-class free "list".

    This speeds up object allocation and freeing when there are many short-lived
    objects.

    TODO: Generalize to support a free list with up to N objects.
    """
    assert cl.reuse_freed_instance
    context = c_emitter.context
    name = cl.name_prefix(c_emitter.names) + "_free_instance"
    struct_name = cl.struct_name(c_emitter.names)
    # Not exported: the free-instance slot is only read/written by the class's
    # own setup/dealloc code, which lives in the defining group. Exporting it
    # also trips a C diagnostic under `Py_GIL_DISABLED`, where `CPyThreadLocal`
    # expands to `__thread` and can't legally appear inside the exports struct.
    context.declarations[name] = HeaderDeclaration(f"CPyThreadLocal {struct_name} *{name};")

