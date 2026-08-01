
def get_all_type_vars(tp: Type) -> list[TypeVarLikeType]:
    # TODO: should we always use this function instead of get_type_vars() above?
    return tp.accept(TypeVarExtractor(include_all=True))

