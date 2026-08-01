
def find_non_acyclic_base(cdef: ClassDef, mapper: Mapper) -> str | None:
    if cdef.type_args:
        return "typing.Generic"

    for expr in cdef.removed_base_type_exprs:
        if fullname := get_removed_base_fullname(expr):
            return fullname
        return "a removed base class"

    for base in cdef.info.mro[1:]:
        if base.fullname == "builtins.object":
            continue

        base_ir = mapper.type_to_ir.get(base)
        if base_ir is not None and base_ir.is_acyclic:
            continue

        return base.fullname

    return None

