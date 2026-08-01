
def generate_vtables(
    base: ClassIR, vtable_setup_name: str, vtable_name: str, emitter: Emitter, shadow: bool
) -> str:
    """Emit the vtables and vtable setup functions for a class.

    This includes both the primary vtable and any trait implementation vtables.
    The trait vtables go before the main vtable, and have the following layout:
        {
            CPyType_T1,         // pointer to type object
            C_T1_trait_vtable,  // pointer to array of method pointers
            C_T1_offset_table,  // pointer to array of attribute offsets
            CPyType_T2,
            C_T2_trait_vtable,
            C_T2_offset_table,
            ...
        }
    The method implementations are calculated at the end of IR pass, attribute
    offsets are {offsetof(native__C, _x1), offsetof(native__C, _y1), ...}.

    To account for both dynamic loading and dynamic class creation,
    vtables are populated dynamically at class creation time, so we
    emit empty array definitions to store the vtables and a function to
    populate them.

    If shadow is True, generate "shadow vtables" that point to the
    shadow glue methods (which should dispatch via the Python C-API).

    Returns the expression to use to refer to the vtable, which might be
    different than the name, if there are trait vtables.
    """

    def trait_vtable_name(trait: ClassIR) -> str:
        return "{}_{}_trait_vtable{}".format(
            base.name_prefix(emitter.names),
            trait.name_prefix(emitter.names),
            "_shadow" if shadow else "",
        )

    def trait_offset_table_name(trait: ClassIR) -> str:
        return "{}_{}_offset_table".format(
            base.name_prefix(emitter.names), trait.name_prefix(emitter.names)
        )

    # Emit array definitions with enough space for all the entries
    emitter.emit_line(
        "static CPyVTableItem {}[{}];".format(
            vtable_name, max(1, len(base.vtable_entries) + 3 * len(base.trait_vtables))
        )
    )

    for trait, vtable in base.trait_vtables.items():
        # Trait methods entry (vtable index -> method implementation).
        emitter.emit_line(
            f"static CPyVTableItem {trait_vtable_name(trait)}[{max(1, len(vtable))}];"
        )
        # Trait attributes entry (attribute number in trait -> offset in actual struct).
        emitter.emit_line(
            "static size_t {}[{}];".format(
                trait_offset_table_name(trait), max(1, len(trait.attributes))
            )
        )

    # Emit vtable setup function
    emitter.emit_line("static bool")
    emitter.emit_line(f"{NATIVE_PREFIX}{vtable_setup_name}(void)")
    emitter.emit_line("{")

    if base.allow_interpreted_subclasses and not shadow:
        emitter.emit_line(f"{NATIVE_PREFIX}{vtable_setup_name}_shadow();")

    subtables = []
    for trait, vtable in base.trait_vtables.items():
        name = trait_vtable_name(trait)
        offset_name = trait_offset_table_name(trait)
        generate_vtable(vtable, name, emitter, [], shadow)
        generate_offset_table(offset_name, emitter, trait, base)
        subtables.append((trait, name, offset_name))

    generate_vtable(base.vtable_entries, vtable_name, emitter, subtables, shadow)

    emitter.emit_line("return 1;")
    emitter.emit_line("}")

    return vtable_name if not subtables else f"{vtable_name} + {len(subtables) * 3}"

