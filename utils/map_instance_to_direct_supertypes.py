
def map_instance_to_direct_supertypes(instance: Instance, supertype: TypeInfo) -> list[Instance]:
    # FIX: There should only be one supertypes, always.
    typ = instance.type
    result: list[Instance] = []

    for b in typ.bases:
        if b.type == supertype:

            if supertype.fullname == "builtins.tuple" and instance.type.tuple_type:
                if has_type_vars(instance.type.tuple_type):
                    # We special case mapping generic tuple types to tuple base, because for
                    # such tuples fallback can't be calculated before applying type arguments.
                    alias = instance.type.special_alias
                    assert alias is not None
                    if not alias._is_recursive:
                        # Unfortunately we can't support this for generic recursive tuples.
                        # If we skip this special casing we will fall back to tuple[Any, ...].
                        tuple_type = expand_type_by_instance(instance.type.tuple_type, instance)
                        if isinstance(tuple_type, TupleType):
                            # Make the import here to avoid cyclic imports.
                            import mypy.typeops

                            result.append(mypy.typeops.tuple_fallback(tuple_type))
                            continue
                        elif isinstance(tuple_type, Instance):
                            # This can happen after normalizing variadic tuples.
                            result.append(tuple_type)
                            continue

            t = expand_type_by_instance(b, instance)
            assert isinstance(t, Instance)
            result.append(t)

    if result:
        return result
    else:
        # Relationship with the supertype not specified explicitly. Use dynamic
        # type arguments implicitly.
        any_type = AnyType(TypeOfAny.unannotated)
        return [Instance(supertype, [any_type] * len(supertype.type_vars))]

