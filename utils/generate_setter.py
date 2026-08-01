
def generate_setter(cl: ClassIR, attr: str, rtype: RType, emitter: Emitter) -> None:
    attr_field = emitter.attr(attr)
    emitter.emit_line("static int")
    emitter.emit_line(
        "{}({} *self, PyObject *value, void *closure)".format(
            setter_name(cl, attr, emitter.names), cl.struct_name(emitter.names)
        )
    )
    emitter.emit_line("{")

    deletable = cl.is_deletable(attr)
    if not deletable:
        emitter.emit_line("if (value == NULL) {")
        emitter.emit_line("PyErr_SetString(PyExc_AttributeError,")
        emitter.emit_line(
            f'    "{repr(cl.name)} object attribute {repr(attr)} cannot be deleted");'
        )
        emitter.emit_line("return -1;")
        emitter.emit_line("}")

    if IS_FREE_THREADED and is_simple_refcounted_pointer(rtype):
        # In free-threaded builds, publish the new value atomically via
        # CPy_SetAttrRef so a concurrent reader (see CPy_GetAttrRef) never sees a
        # torn pointer or a freed old value. CPy_SetAttrRef steals its value and
        # reclaims the old one, so we cast/type-check the incoming value, take a
        # new reference (the setter only borrows 'value'), then hand it over.
        # A NULL value deletes the attribute (reclaims the old value, stores NULL).
        if deletable:
            emitter.emit_line("if (value != NULL) {")
        if is_same_type(rtype, object_rprimitive):
            emitter.emit_line("PyObject *tmp = value;")
        else:
            emitter.emit_cast("value", "tmp", rtype, declare_dest=True)
            emitter.emit_lines("if (!tmp)", "    return -1;")
        emitter.emit_inc_ref("tmp", rtype)
        emitter.emit_line(f"CPy_SetAttrRef((PyObject **)&self->{attr_field}, tmp);")
        if deletable:
            emitter.emit_line("} else {")
            emitter.emit_line(f"CPy_SetAttrRef((PyObject **)&self->{attr_field}, NULL);")
            emitter.emit_line("}")
        emitter.emit_line("return 0;")
        emitter.emit_line("}")
        return

    # HACK: Don't consider refcounted values as always defined, since it's possible to
    #       access uninitialized values via 'gc.get_objects()'. Accessing non-refcounted
    #       values is benign.
    always_defined = cl.is_always_defined(attr) and not rtype.is_refcounted

    if rtype.is_refcounted:
        attr_expr = f"self->{attr_field}"
        if not always_defined:
            emitter.emit_undefined_attr_check(rtype, attr_expr, "!=", "self", attr, cl)
        emitter.emit_dec_ref(f"self->{attr_field}", rtype)
        if not always_defined:
            emitter.emit_line("}")

    if deletable:
        emitter.emit_line("if (value != NULL) {")

    if rtype.is_unboxed:
        # Borrow the unboxed value: emit_inc_ref below takes the single owned
        # reference, matching the borrowed-then-incref pattern of the other two
        # branches. Without borrow=True, emit_unbox already creates a new
        # reference for refcounted unboxed types (e.g. CPyTagged boxed ints,
        # tuples with refcounted fields), so the emit_inc_ref would double the
        # reference and leak the stored value on every set via this setter.
        emitter.emit_unbox(
            "value", "tmp", rtype, error=ReturnHandler("-1"), declare_dest=True, borrow=True
        )
    elif is_same_type(rtype, object_rprimitive):
        emitter.emit_line("PyObject *tmp = value;")
    else:
        emitter.emit_cast("value", "tmp", rtype, declare_dest=True)
        emitter.emit_lines("if (!tmp)", "    return -1;")
    emitter.emit_inc_ref("tmp", rtype)
    emitter.emit_line(f"self->{attr_field} = tmp;")
    if rtype.error_overlap and not always_defined:
        emitter.emit_attr_bitmap_set("tmp", "self", rtype, cl, attr)

    if deletable:
        emitter.emit_line("} else {")
        emitter.set_undefined_value(f"self->{attr_field}", rtype)
        if rtype.error_overlap:
            emitter.emit_attr_bitmap_clear("self", rtype, cl, attr)
        emitter.emit_line("}")
    emitter.emit_line("return 0;")
    emitter.emit_line("}")

