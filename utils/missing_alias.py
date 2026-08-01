
def missing_alias() -> TypeAlias:
    suggestion = _SUGGESTION.format("alias")
    return TypeAlias(AnyType(TypeOfAny.special_form), suggestion, "<missing>", line=-1, column=-1)

