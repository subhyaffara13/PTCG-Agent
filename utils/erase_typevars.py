
def erase_typevars(t: Type, ids_to_erase: Container[TypeVarId] | None = None) -> Type:
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """

    if ids_to_erase is None:
        return t.accept(TypeVarEraser(None, AnyType(TypeOfAny.special_form)))

    def erase_id(id: TypeVarId) -> bool:
        return id in ids_to_erase

    return t.accept(TypeVarEraser(erase_id, AnyType(TypeOfAny.special_form)))

