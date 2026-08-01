
def generate_offset_table(
    trait_offset_table_name: str, emitter: Emitter, trait: ClassIR, cl: ClassIR
) -> None:
    """Generate attribute offset row of a trait vtable."""
    emitter.emit_line(f"size_t {trait_offset_table_name}_scratch[] = {{")
    for attr in trait.attributes:
        emitter.emit_line(f"offsetof({cl.struct_name(emitter.names)}, {emitter.attr(attr)}),")
    if not trait.attributes:
        # This is for msvc.
        emitter.emit_line("0")
    emitter.emit_line("};")
    emitter.emit_line(
        "memcpy({name}, {name}_scratch, sizeof({name}));".format(name=trait_offset_table_name)
    )

