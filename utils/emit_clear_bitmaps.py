
def emit_clear_bitmaps(cl: ClassIR, emitter: Emitter) -> None:
    """Emit C code to clear bitmaps that track if attributes have an assigned value."""
    for i in range(0, len(cl.bitmap_attrs), BITMAP_BITS):
        field = emitter.bitmap_field(i)
        emitter.emit_line(f"self->{field} = 0;")

