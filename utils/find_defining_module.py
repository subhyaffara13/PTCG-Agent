
def find_defining_module(modules: dict[str, MypyFile], typ: CallableType) -> MypyFile | None:
    if not typ.definition:
        return None
    fullname = typ.definition.fullname
    if "." in fullname:
        for i in range(fullname.count(".")):
            module_name = fullname.rsplit(".", i + 1)[0]
            try:
                return modules[module_name]
            except KeyError:
                pass
        assert False, "Couldn't determine module from CallableType"
    return None

