
def generate_arg_check(
    name: str,
    typ: RType,
    emitter: Emitter,
    error: ErrorHandler | None = None,
    *,
    optional: bool = False,
    raise_exception: bool = True,
    bitmap_arg_index: int = 0,
) -> None:
    """Insert a runtime check for argument and unbox if necessary.

    The object is named PyObject *obj_{}. This is expected to generate
    a value of name arg_{} (unboxed if necessary). For each primitive a runtime
    check ensures the correct type.
    """
    error = error or AssignHandler()
    if typ.is_unboxed:
        if typ.error_overlap and optional:
            # Update bitmap is value is provided.
            init = emitter.c_undefined_value(typ)
            emitter.emit_line(f"{emitter.ctype(typ)} arg_{name} = {init};")
            emitter.emit_line(f"if (obj_{name} != NULL) {{")
            bitmap = bitmap_name(bitmap_arg_index // BITMAP_BITS)
            emitter.emit_line(f"{bitmap} |= 1 << {bitmap_arg_index & (BITMAP_BITS - 1)};")
            emitter.emit_unbox(
                f"obj_{name}",
                f"arg_{name}",
                typ,
                declare_dest=False,
                raise_exception=raise_exception,
                error=error,
                borrow=True,
            )
            emitter.emit_line("}")
        else:
            # Borrow when unboxing to avoid reference count manipulation.
            emitter.emit_unbox(
                f"obj_{name}",
                f"arg_{name}",
                typ,
                declare_dest=True,
                raise_exception=raise_exception,
                error=error,
                borrow=True,
                optional=optional,
            )
    elif is_object_rprimitive(typ):
        # Object is trivial since any object is valid
        if optional:
            emitter.emit_line(f"PyObject *arg_{name};")
            emitter.emit_line(f"if (obj_{name} == NULL) {{")
            emitter.emit_line(f"arg_{name} = {emitter.c_error_value(typ)};")
            emitter.emit_lines("} else {", f"arg_{name} = obj_{name}; ", "}")
        else:
            emitter.emit_line(f"PyObject *arg_{name} = obj_{name};")
    else:
        emitter.emit_cast(
            f"obj_{name}",
            f"arg_{name}",
            typ,
            declare_dest=True,
            raise_exception=raise_exception,
            error=error,
            optional=optional,
        )

