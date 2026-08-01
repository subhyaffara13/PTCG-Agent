
def get_proper_type(typ: None) -> None: ...


def get_proper_type(typ: Type) -> ProperType: ...


def get_proper_type(typ: Type | None) -> ProperType | None:
    """Get the expansion of a type alias type.

    If the type is already a proper type, this is a no-op. Use this function
    wherever a decision is made on a call like e.g. 'if isinstance(typ, UnionType): ...',
    because 'typ' in this case may be an alias to union. Note: if after making the decision
    on the isinstance() call you pass on the original type (and not one of its components)
    it is recommended to *always* pass on the unexpanded alias.
    """
    if typ is None:
        return None
    # TODO: this is an ugly hack, remove.
    if isinstance(typ, TypeGuardedType):
        typ = typ.type_guard
    while isinstance(typ, TypeAliasType):
        typ = typ._expand_once()
    # TODO: store the name of original type alias on this type, so we can show it in errors.
    return cast(ProperType, typ)

