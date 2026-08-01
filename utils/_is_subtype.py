
def _is_subtype(
    left: Type, right: Type, subtype_context: SubtypeContext, proper_subtype: bool
) -> bool:
    subtype_context.check_context(proper_subtype)
    orig_right = right
    orig_left = left
    left = get_proper_type(left)
    right = get_proper_type(right)

    # Note: Unpack type should not be a subtype of Any, since it may represent
    # multiple types. This should always go through the visitor, to check arity.
    if (
        not proper_subtype
        and isinstance(right, (AnyType, UnboundType, ErasedType))
        and not isinstance(left, UnpackType)
    ):
        # TODO: should we consider all types proper subtypes of UnboundType and/or
        # ErasedType as we do for non-proper subtyping.
        return True

    # Cases specific w.r.t. right type are easier to handle before entering the SubtypeVisitor.
    # Currently, these include Union types and TypeVarType with values.
    if isinstance(right, UnionType) and not isinstance(left, UnionType):
        # Normally, when 'left' is not itself a union, the only way
        # 'left' can be a subtype of the union 'right' is if it is a
        # subtype of one of the items making up the union.
        if proper_subtype:
            is_subtype_of_item = any(
                is_proper_subtype(orig_left, item, subtype_context=subtype_context)
                for item in right.items
            )
        else:
            is_subtype_of_item = any(
                is_subtype(orig_left, item, subtype_context=subtype_context)
                for item in right.items
            )
        # Recombine rhs literal types, to make an enum type a subtype
        # of a union of all enum items as literal types. Only do it if
        # the previous check didn't succeed, since recombining can be
        # expensive.
        # `bool` is a special case, because `bool` is `Literal[True, False]`.
        if (
            not is_subtype_of_item
            and isinstance(left, Instance)
            and (left.type.is_enum or left.type.fullname == "builtins.bool")
        ):
            right = UnionType(
                mypy.typeops.try_contracting_literals_in_union(flatten_nested_unions(right.items))
            )
            if proper_subtype:
                is_subtype_of_item = any(
                    is_proper_subtype(orig_left, item, subtype_context=subtype_context)
                    for item in right.items
                )
            else:
                is_subtype_of_item = any(
                    is_subtype(orig_left, item, subtype_context=subtype_context)
                    for item in right.items
                )
        # However, if 'left' is a type variable T, T might also have
        # an upper bound which is itself a union. This case will be
        # handled below by the SubtypeVisitor. We have to check both
        # possibilities, to handle both cases like T <: Union[T, U]
        # and cases like T <: B where B is the upper bound of T and is
        # a union. (See #2314.)
        if not isinstance(left, TypeVarType):
            return is_subtype_of_item
        elif is_subtype_of_item:
            return True
        # otherwise, fall through

    if isinstance(right, TypeVarType) and right.values and not isinstance(left, TypeVarType):
        if proper_subtype:
            if all(
                is_proper_subtype(orig_left, v, subtype_context=subtype_context)
                for v in right.values
            ):
                return True
        elif all(is_subtype(orig_left, v, subtype_context=subtype_context) for v in right.values):
            return True

    return left.accept(SubtypeVisitor(orig_right, subtype_context, proper_subtype))

