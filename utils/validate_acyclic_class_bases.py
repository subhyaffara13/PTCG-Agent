
def validate_acyclic_class_bases(
    path: str, cdef: ClassDef, errors: Errors, mapper: Mapper
) -> None:
    ir = mapper.type_to_ir[cdef.info]
    if not ir.is_acyclic:
        return

    if fullname := find_non_acyclic_base(cdef, mapper):
        errors.error(
            f'"acyclic" can\'t be used in a class that inherits from non-acyclic type "{fullname}"',
            path,
            cdef.line,
        )

