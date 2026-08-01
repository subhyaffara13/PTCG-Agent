
def emit_reuse_dealloc(cl: ClassIR, emitter: Emitter) -> None:
    """Emit code to deallocate object by putting it to per-type free list.

    The free "list" currently can have up to one object.
    """
    prefix = cl.name_prefix(emitter.names)
    emitter.emit_line(f"if ({prefix}_free_instance == NULL) {{")
    emitter.emit_line(f"{prefix}_free_instance = self;")

    # Clear attributes and free referenced objects.

    emit_clear_bitmaps(cl, emitter)

    for base in reversed(cl.base_mro):
        for attr, rtype in base.attributes.items():
            emitter.emit_reuse_clear(f"self->{emitter.attr(attr)}", rtype)

    emitter.emit_line("return;")
    emitter.emit_line("}")

