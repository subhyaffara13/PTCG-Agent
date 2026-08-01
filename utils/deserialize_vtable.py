
def deserialize_vtable(data: list[JsonDict], ctx: DeserMaps) -> VTableEntries:
    return [deserialize_vtable_entry(x, ctx) for x in data]

