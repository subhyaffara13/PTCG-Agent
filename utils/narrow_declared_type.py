
def narrow_declared_type(declared: Type, narrowed: Type) -> Type:
    """Return the declared type narrowed down to another type."""
    # TODO: check infinite recursion for aliases here.
    if isinstance(narrowed, TypeGuardedType):
        # A type guard forces the new type even if it doesn't overlap the old...
        if is_proper_subtype(declared, narrowed.type_guard, ignore_promotions=True):
            # ...unless it is a proper supertype of declared type.
            return declared
        return narrowed.type_guard

    original_declared = declared
    original_narrowed = narrowed
    declared = get_proper_type(declared)
    narrowed = get_proper_type(narrowed)

    if declared == narrowed:
        return original_declared
    if isinstance(declared, UnionType):
        declared_items = declared.relevant_items()
        if isinstance(narrowed, UnionType):
            narrowed_items = narrowed.relevant_items()
        else:
            narrowed_items = [narrowed]
        return make_simplified_union(
            [
                narrow_declared_type(d, n)
                for d in declared_items
                for n in narrowed_items
                # This (ugly) special-casing is needed to support checking
                # branches like this:
                # x: Union[float, complex]
                # if isinstance(x, int):
                #     ...
                # And assignments like this:
                # x: float | None
                # y: int | None
                # x = y
                if (
                    is_overlapping_types(d, n, ignore_promotions=True)
                    or is_subtype(n, d, ignore_promotions=False)
                )
            ]
        )
    if is_enum_overlapping_union(declared, narrowed):
        # Quick check before reaching `is_overlapping_types`. If it's enum/literal overlap,
        # avoid full expansion and make it faster.
        assert isinstance(narrowed, UnionType)
        return make_simplified_union(
            [narrow_declared_type(declared, x) for x in narrowed.relevant_items()]
        )
    elif (
        isinstance(declared, TypeVarType)
        and not has_type_vars(original_narrowed)
        and is_subtype(original_narrowed, declared.upper_bound)
    ):
        # We put this branch early to get T(bound=Union[A, B]) instead of
        # Union[T(bound=A), T(bound=B)] that will be confusing for users.
        return declared.copy_modified(
            upper_bound=narrow_declared_type(declared.upper_bound, original_narrowed)
        )
    elif (
        isinstance(narrowed, TypeVarType)
        and not has_type_vars(original_declared)
        and is_subtype(original_declared, narrowed.upper_bound)
    ):
        # This branch is a mirror image of the above one.
        return narrowed.copy_modified(
            upper_bound=narrow_declared_type(original_declared, narrowed.upper_bound)
        )
    elif not is_overlapping_types(declared, narrowed):
        if state.strict_optional:
            return UninhabitedType()
        else:
            return NoneType()
    elif isinstance(narrowed, UnionType):
        return make_simplified_union(
            [narrow_declared_type(declared, x) for x in narrowed.relevant_items()]
        )
    elif isinstance(narrowed, AnyType):
        return original_narrowed
    elif isinstance(narrowed, TypeVarType) and is_subtype(narrowed.upper_bound, declared):
        return narrowed
    elif isinstance(declared, TypeType) and isinstance(narrowed, TypeType):
        return TypeType.make_normalized(
            narrow_declared_type(declared.item, narrowed.item),
            is_type_form=declared.is_type_form and narrowed.is_type_form,
        )
    elif (
        isinstance(declared, TypeType)
        and isinstance(narrowed, Instance)
        and narrowed.type.is_metaclass()
    ):
        if declared.is_type_form:
            # The declared TypeForm[T] after narrowing must be a kind of
            # type object at least as narrow as Type[T]
            return narrow_declared_type(
                TypeType.make_normalized(
                    declared.item, line=declared.line, column=declared.column, is_type_form=False
                ),
                original_narrowed,
            )
        # We'd need intersection types, so give up.
        return original_declared
    elif isinstance(declared, Instance):
        if declared.type.alt_promote:
            # Special case: low-level integer type can't be narrowed
            return original_declared
        if (
            isinstance(narrowed, Instance)
            and narrowed.type.alt_promote
            and narrowed.type.alt_promote.type is declared.type
        ):
            # Special case: 'int' can't be narrowed down to a native int type such as
            # i64, since they have different runtime representations.
            return original_declared
        return meet_types(original_declared, original_narrowed)
    elif isinstance(declared, (TupleType, TypeType, LiteralType)):
        return meet_types(original_declared, original_narrowed)
    elif isinstance(declared, TypedDictType) and isinstance(narrowed, Instance):
        # Special case useful for selecting TypedDicts from unions using isinstance(x, dict).
        if narrowed.type.fullname == "builtins.dict" and all(
            isinstance(t, AnyType) for t in get_proper_types(narrowed.args)
        ):
            return original_declared
        return meet_types(original_declared, original_narrowed)
    elif (
        isinstance(declared, CallableType)
        and isinstance(narrowed, CallableType)
        and has_type_vars(declared.ret_type)
    ):
        return narrowed.copy_modified(
            ret_type=narrow_declared_type(declared.ret_type, narrowed.ret_type)
        )

    return original_narrowed

