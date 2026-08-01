
def map_type_from_supertype(typ: Type, sub_info: TypeInfo, super_info: TypeInfo) -> Type:
    """Map type variables in a type defined in a supertype context to be valid
    in the subtype context. Assume that the result is unique; if more than
    one type is possible, return one of the alternatives.

    For example, assume

      class D(Generic[S]): ...
      class C(D[E[T]], Generic[T]): ...

    Now S in the context of D would be mapped to E[T] in the context of C.
    """
    # Create the type of self in subtype, of form t[a1, ...].
    inst_type = fill_typevars(sub_info)
    if isinstance(inst_type, TupleType):
        inst_type = tuple_fallback(inst_type)
    # Map the type of self to supertype. This gets us a description of the
    # supertype type variables in terms of subtype variables, i.e. t[t1, ...]
    # so that any type variables in tN are to be interpreted in subtype
    # context.
    inst_type = map_instance_to_supertype(inst_type, super_info)
    # Finally expand the type variables in type with those in the previously
    # constructed type. Note that both type and inst_type may have type
    # variables, but in type they are interpreted in supertype context while
    # in inst_type they are interpreted in subtype context. This works even if
    # the names of type variables in supertype and subtype overlap.
    return expand_type_by_instance(typ, inst_type)

