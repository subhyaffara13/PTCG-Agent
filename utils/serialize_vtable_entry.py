
def serialize_vtable_entry(entry: VTableMethod) -> JsonDict:
    return {
        ".class": "VTableMethod",
        "cls": entry.cls.fullname,
        "name": entry.name,
        "method": entry.method.decl.id,
        "shadow_method": entry.shadow_method.decl.id if entry.shadow_method else None,
    }

