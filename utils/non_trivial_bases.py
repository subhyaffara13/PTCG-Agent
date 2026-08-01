
def non_trivial_bases(info: TypeInfo) -> list[TypeInfo]:
    return [base for base in info.mro[1:] if base.fullname != "builtins.object"]

