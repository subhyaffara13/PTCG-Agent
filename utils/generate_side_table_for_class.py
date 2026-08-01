
def generate_side_table_for_class(
    cl: ClassIR, name: str, type: str, slots: dict[str, str], emitter: Emitter
) -> str | None:
    name = f"{cl.name_prefix(emitter.names)}_{name}"
    emitter.emit_line(f"static {type} {name} = {{")
    for field, value in slots.items():
        emitter.emit_line(f".{field} = {value},")
    emitter.emit_line("};")
    return name

