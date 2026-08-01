
def deserialize_vtable_entry(data: JsonDict, ctx: DeserMaps) -> VTableMethod:
    if data[".class"] == "VTableMethod":
        return VTableMethod(
            ctx.classes[data["cls"]],
            data["name"],
            ctx.functions[data["method"]],
            ctx.functions[data["shadow_method"]] if data["shadow_method"] else None,
        )
    assert False, "Bogus vtable .class: %s" % data[".class"]

