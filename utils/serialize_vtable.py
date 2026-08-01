
def serialize_vtable(vtable: VTableEntries) -> list[JsonDict]:
    return [serialize_vtable_entry(v) for v in vtable]

