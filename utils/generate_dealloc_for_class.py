
def generate_dealloc_for_class(
    cl: ClassIR,
    dealloc_func_name: str,
    clear_func_name: str,
    has_tp_finalize: bool,
    emitter: Emitter,
) -> None:
    emitter.emit_line("static void")
    emitter.emit_line(f"{dealloc_func_name}({cl.struct_name(emitter.names)} *self)")
    emitter.emit_line("{")
    if has_tp_finalize:
        emitter.emit_line("PyObject *type, *value, *traceback;")
        emitter.emit_line("PyErr_Fetch(&type, &value, &traceback);")
        emitter.emit_line("int res = PyObject_CallFinalizerFromDealloc((PyObject *)self);")
        # CPython interpreter uses PyErr_WriteUnraisable: https://docs.python.org/3/c-api/exceptions.html#c.PyErr_WriteUnraisable
        # However, the message is slightly different due to the way mypyc compiles classes.
        # CPython interpreter prints: Exception ignored in: <function F.__del__ at 0x100aed940>
        # mypyc prints: Exception ignored in: <slot wrapper '__del__' of 'F' objects>
        emitter.emit_line("if (PyErr_Occurred() != NULL) {")
        # Don't untrack instance if error occurred
        emitter.emit_line("PyErr_WriteUnraisable((PyObject *)self);")
        emitter.emit_line("res = -1;")
        emitter.emit_line("}")
        emitter.emit_line("PyErr_Restore(type, value, traceback);")
        emitter.emit_line("if (res < 0) {")
        emitter.emit_line("goto done;")
        emitter.emit_line("}")
    if not cl.is_acyclic:
        emitter.emit_line("PyObject_GC_UnTrack(self);")
    if cl.builtin_base:
        emitter.emit_line(f"{clear_func_name}(self);")
        # For native subclasses of builtins such as dict, the base deallocator
        # is responsible for tearing down base-owned storage and freeing memory.
        # Re-track self if base is GC-aware to match cpython's subtype_dealloc.
        base = f"{emitter.type_struct_name(cl)}->tp_base"
        base_arg = "(PyObject *)self"
        emitter.emit_line(f"if (PyType_IS_GC({base})) PyObject_GC_Track({base_arg});")
        emitter.emit_base_tp_function_call(cl, "tp_dealloc", base_arg)
        emitter.emit_line("done: ;")
        emitter.emit_line("}")
        return
    if cl.reuse_freed_instance:
        emit_reuse_dealloc(cl, emitter)
    # The trashcan is needed to handle deep recursive deallocations
    emitter.emit_line(f"CPy_TRASHCAN_BEGIN(self, {dealloc_func_name})")
    emitter.emit_line(f"{clear_func_name}(self);")
    emitter.emit_line("Py_TYPE(self)->tp_free((PyObject *)self);")
    emitter.emit_line("CPy_TRASHCAN_END(self)")
    emitter.emit_line("done: ;")
    emitter.emit_line("}")

