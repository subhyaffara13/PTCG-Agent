
def generate_getter(cl: ClassIR, attr: str, rtype: RType, emitter: Emitter) -> None:
    attr_field = emitter.attr(attr)
    emitter.emit_line("static PyObject *")
    emitter.emit_line(
        "{}({} *self, void *closure)".format(
            getter_name(cl, attr, emitter.names), cl.struct_name(emitter.names)
        )
    )
    emitter.emit_line("{")
    attr_expr = f"self->{attr_field}"

    if IS_FREE_THREADED and is_simple_refcounted_pointer(rtype):
        # In free-threaded builds, load the attribute and take a new reference
        # atomically to avoid a use-after-free race with a concurrent setter.
        # CPy_GetAttrRef returns NULL if the attribute is undefined (NULL field),
        # which is exactly the error/undefined value for a 'PyObject *' field.
        #
        # Final attributes are never rebound (no setter), so there is no concurrent
        # writer to race with: a plain load + incref is safe. Use the cheaper
        # CPy_GetAttrRefFinal, which skips the try-incref and _Py_NewRefWithLock
        # slow path entirely (an unconditional Py_INCREF needs no maybe-weakref).
        # This getter is generated per defining class, so a direct membership test
        # matches the read-only getset table above (no need to walk the MRO).
        if attr in cl.final_attributes:
            getattr_ref = f"CPy_GetAttrRefFinal((PyObject **)&{attr_expr})"
        else:
            getattr_ref = f"CPy_GetAttrRef((PyObject **)&{attr_expr})"
        emitter.emit_line(f"PyObject *retval = {getattr_ref};")
        emitter.emit_line("if (unlikely(retval == NULL)) {")
        emitter.emit_line("PyErr_SetString(PyExc_AttributeError,")
        emitter.emit_line(f'    "attribute {repr(attr)} of {repr(cl.name)} undefined");')
        emitter.emit_line("return NULL;")
        emitter.emit_line("}")
        emitter.emit_line("return retval;")
        emitter.emit_line("}")
        return

    # HACK: Don't consider refcounted values as always defined, since it's possible to
    #       access uninitialized values via 'gc.get_objects()'. Accessing non-refcounted
    #       values is benign.
    always_defined = cl.is_always_defined(attr) and not rtype.is_refcounted

    if not always_defined:
        emitter.emit_undefined_attr_check(rtype, attr_expr, "==", "self", attr, cl, unlikely=True)
        emitter.emit_line("PyErr_SetString(PyExc_AttributeError,")
        emitter.emit_line(f'    "attribute {repr(attr)} of {repr(cl.name)} undefined");')
        emitter.emit_line("return NULL;")
        emitter.emit_line("}")
    emitter.emit_inc_ref(f"self->{attr_field}", rtype)
    emitter.emit_box(f"self->{attr_field}", "retval", rtype, declare_dest=True)
    emitter.emit_line("return retval;")
    emitter.emit_line("}")

