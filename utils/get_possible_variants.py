
def get_possible_variants(typ: Type) -> list[Type]:
    """This function takes any "Union-like" type and returns a list of the available "options".

    Specifically, there are currently exactly three different types that can have
    "variants" or are "union-like":

    - Unions
    - TypeVars with value restrictions
    - Overloads

    This function will return a list of each "option" present in those types.

    If this function receives any other type, we return a list containing just that
    original type. (E.g. pretend the type was contained within a singleton union).

    The only current exceptions are regular TypeVars and ParamSpecs. For these "TypeVarLike"s,
    we return a list containing that TypeVarLike's upper bound.

    This function is useful primarily when checking to see if two types are overlapping:
    the algorithm to check if two unions are overlapping is fundamentally the same as
    the algorithm for checking if two overloads are overlapping.

    Normalizing both kinds of types in the same way lets us reuse the same algorithm
    for both.
    """
    typ = get_proper_type(typ)

    if isinstance(typ, TypeVarType):
        if len(typ.values) > 0:
            return typ.values
        else:
            return [typ.upper_bound]
    elif isinstance(typ, ParamSpecType):
        # Extract 'object' from the final mro item
        upper_bound = get_proper_type(typ.upper_bound)
        if isinstance(upper_bound, Instance):
            return [Instance(upper_bound.type.mro[-1], [])]
        return [AnyType(TypeOfAny.implementation_artifact)]
    elif isinstance(typ, TypeVarTupleType):
        return [typ.upper_bound]
    elif isinstance(typ, UnionType):
        return list(typ.items)
    elif isinstance(typ, Overloaded):
        # Note: doing 'return typ.items()' makes mypy
        # infer a too-specific return type of List[CallableType]
        return list(typ.items)
    else:
        return [typ]

