
def enum_object_hook(obj: dict[str, Any]) -> Enum | dict[str, Any]:
    if "__enum__" in obj:
        modname, _, classname = obj["fqn"].partition(":")
        mod = importlib.import_module(modname)
        enum_cls = mod
        for attr in classname.split("."):
            enum_cls = getattr(enum_cls, attr)
        enum_cls = cast(type[Enum], enum_cls)

        return enum_cls[obj["name"]]
    return obj

