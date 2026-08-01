
def get_proper_types(types: list[Type] | tuple[Type, ...]) -> list[ProperType]: ...


def get_proper_types(
    types: list[Type | None] | tuple[Type | None, ...],
) -> list[ProperType | None]: ...


def get_proper_types(
    types: list[Type] | list[Type | None] | tuple[Type | None, ...],
) -> list[ProperType] | list[ProperType | None]:
    if isinstance(types, list):
        typelist = types
        # Optimize for the common case so that we don't need to allocate anything
        if not any(isinstance(t, (TypeAliasType, TypeGuardedType)) for t in typelist):
            return cast("list[ProperType]", typelist)
        return [get_proper_type(t) for t in typelist]
    else:
        return [get_proper_type(t) for t in types]

