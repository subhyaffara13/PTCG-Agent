
def map_instance_to_supertypes(instance: Instance, supertype: TypeInfo) -> list[Instance]:
    # FIX: Currently we should only have one supertype per interface, so no
    #      need to return an array
    result: list[Instance] = []
    for path in class_derivation_paths(instance.type, supertype):
        types = [instance]
        for sup in path:
            a: list[Instance] = []
            for t in types:
                a.extend(map_instance_to_direct_supertypes(t, sup))
            types = a
        result.extend(types)
    if result:
        return result
    else:
        # Nothing. Presumably due to an error. Construct a dummy using Any.
        any_type = AnyType(TypeOfAny.from_error)
        return [Instance(supertype, [any_type] * len(supertype.type_vars))]

