
def fill_typevars_with_any(typ: TypeInfo) -> Instance | TupleType:
    """Apply a correct number of Any's as type arguments to a type."""
    inst = Instance(typ, erased_vars(typ.defn.type_vars, TypeOfAny.special_form))
    if typ.tuple_type is None:
        return inst
    erased_tuple_type = erase_typevars(typ.tuple_type, {tv.id for tv in typ.defn.type_vars})
    assert isinstance(erased_tuple_type, ProperType)
    if isinstance(erased_tuple_type, TupleType):
        return typ.tuple_type.copy_modified(fallback=inst)
    return inst

