
def generate_vtable(
    entries: VTableEntries,
    vtable_name: str,
    emitter: Emitter,
    subtables: list[tuple[ClassIR, str, str]],
    shadow: bool,
) -> None:
    emitter.emit_line(f"CPyVTableItem {vtable_name}_scratch[] = {{")
    if subtables:
        emitter.emit_line("/* Array of trait vtables */")
        for trait, table, offset_table in subtables:
            emitter.emit_line(
                "(CPyVTableItem){}, (CPyVTableItem){}, (CPyVTableItem){},".format(
                    emitter.type_struct_name(trait), table, offset_table
                )
            )
        emitter.emit_line("/* Start of real vtable */")

    for entry in entries:
        method = entry.shadow_method if shadow and entry.shadow_method else entry.method
        emitter.emit_line(
            "(CPyVTableItem){}{}{},".format(
                emitter.get_group_prefix(entry.method.decl),
                NATIVE_PREFIX,
                method.cname(emitter.names),
            )
        )

    # msvc doesn't allow empty arrays; maybe allowing them at all is an extension?
    if not entries:
        emitter.emit_line("NULL")
    emitter.emit_line("};")
    emitter.emit_line("memcpy({name}, {name}_scratch, sizeof({name}));".format(name=vtable_name))

