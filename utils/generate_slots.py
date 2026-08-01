
def generate_slots(cl: ClassIR, table: SlotTable, emitter: Emitter) -> dict[str, str]:
    fields: dict[str, str] = {}
    generated: dict[str, str] = {}
    # Sort for determinism on Python 3.5
    for name, (slot, generator) in sorted(table.items(), key=lambda x: slot_key(x[0])):
        method_cls = cl.get_method_and_class(name)
        if method_cls and (method_cls[1] == cl or name in ALWAYS_FILL):
            if slot in generated:
                # Reuse previously generated wrapper.
                fields[slot] = generated[slot]
            else:
                # Generate new wrapper.
                name = generator(cl, method_cls[0], emitter)
                fields[slot] = name
                generated[slot] = name

    return fields

