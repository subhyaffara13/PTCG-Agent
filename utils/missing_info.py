
def missing_info(modules: dict[str, MypyFile]) -> TypeInfo:
    suggestion = _SUGGESTION.format("info")
    dummy_def = ClassDef(suggestion, Block([]))
    dummy_def.fullname = suggestion

    info = TypeInfo(SymbolTable(), dummy_def, "<missing>")
    obj_type = lookup_fully_qualified_typeinfo(modules, "builtins.object", allow_missing=False)
    info.bases = [Instance(obj_type, [])]
    info.mro = [info, obj_type]
    return info

