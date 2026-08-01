
def get_type_vars(tp: Type) -> list[TypeVarType]:
    return cast("list[TypeVarType]", tp.accept(TypeVarExtractor()))

