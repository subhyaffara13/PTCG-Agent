
def conditional_types(
    current_type: Type,
    proposed_type_ranges: list[TypeRange] | None,
    default: None = None,
    *,
    consider_runtime_isinstance: bool = True,
    from_equality: bool = False,
) -> tuple[Type | None, Type | None]: ...


def conditional_types(
    current_type: Type,
    proposed_type_ranges: list[TypeRange] | None,
    default: Type,
    *,
    consider_runtime_isinstance: bool = True,
    from_equality: bool = False,
) -> tuple[Type, Type]: ...


def conditional_types(
    current_type: Type,
    proposed_type_ranges: list[TypeRange] | None,
    default: Type | None = None,
    *,
    consider_runtime_isinstance: bool = True,
    from_equality: bool = False,
) -> tuple[Type | None, Type | None]:
    """Takes in the current type and a proposed type of an expression.

    Returns a 2-tuple:
        The first element is the proposed type, if the expression can be the proposed type.
            (or default, if default is set and the expression is a subtype of the proposed type).
        The second element is the type it would hold if it was not the proposed type, if any.
            (or default, if default is set and the expression is not a subtype of the proposed type).

        UninhabitedType means unreachable.
        None means no new information can be inferred.
    """
    if proposed_type_ranges is None:
        # An isinstance check, but we don't understand the type
        return current_type, default

    if not proposed_type_ranges:
        # This is the case for `if isinstance(x, ())` which always returns False.
        return UninhabitedType(), default

    if len(proposed_type_ranges) == 1:
        # expand e.g. bool -> Literal[True] | Literal[False]
        target = proposed_type_ranges[0].item
        target = get_proper_type(target)
        if isinstance(target, LiteralType) and (
            target.is_enum_literal() or isinstance(target.value, bool)
        ):
            enum_name = target.fallback.type.fullname
            current_type = try_expanding_sum_type_to_union(current_type, enum_name)

    proposed_type: Type
    remaining_type: Type

    p_current_type = get_proper_type(current_type)
    # factorize over union types: isinstance(A|B, C) -> yes = A_yes | B_yes
    if isinstance(p_current_type, UnionType):
        yes_items: list[Type] = []
        no_items: list[Type] = []
        for union_item in p_current_type.items:
            yes_type, no_type = conditional_types(
                union_item,
                proposed_type_ranges,
                default=union_item,
                consider_runtime_isinstance=consider_runtime_isinstance,
                from_equality=from_equality,
            )
            yes_items.append(yes_type)
            no_items.append(no_type)

        proposed_type = make_simplified_union(yes_items)
        remaining_type = make_simplified_union(no_items)
        return proposed_type, remaining_type

    proposed_type = make_simplified_union([type_range.item for type_range in proposed_type_ranges])
    items = proposed_type.items if isinstance(proposed_type, UnionType) else [proposed_type]
    for i in range(len(items)):
        item = get_proper_type(items[i])
        # Avoid ever narrowing to a NewType. The principle is values of NewType should only be
        # produce by explicit wrapping
        while isinstance(item, Instance) and item.type.is_newtype:
            item = item.type.bases[0]
        items[i] = item
    proposed_type = get_proper_type(UnionType.make_union(items))

    if isinstance(p_current_type, AnyType):
        return proposed_type, current_type
    if isinstance(proposed_type, AnyType):
        # We don't really know much about the proposed type, so we shouldn't
        # attempt to narrow anything. Instead, we broaden the expr to Any to
        # avoid false positives
        return proposed_type, default
    if not any(type_range.is_upper_bound for type_range in proposed_type_ranges):
        # concrete subtype
        if is_proper_subtype(current_type, proposed_type, ignore_promotions=True):
            return default, UninhabitedType()

        # structural subtypes
        if (
            isinstance(proposed_type, CallableType)
            or (isinstance(proposed_type, Instance) and proposed_type.type.is_protocol)
        ) and is_subtype(current_type, proposed_type, ignore_promotions=True):
            # Note: It's possible that current_type=`Any | Proto` while proposed_type=`Proto`
            #  so we cannot return `Never` for the else branch
            remainder = restrict_subtype_away(
                current_type,
                default if default is not None else proposed_type,
                consider_runtime_isinstance=consider_runtime_isinstance,
            )
            return default, remainder

    if from_equality:
        # We erase generic args because values with different generic types can compare equal
        # For instance, cast(list[str], []) and cast(list[int], [])
        proposed_type = shallow_erase_type_for_equality(proposed_type)

    if not is_overlapping_types(current_type, proposed_type, ignore_promotions=True):
        # Expression is never of any type in proposed_type_ranges
        return UninhabitedType(), default

    # we can only restrict when the type is precise, not bounded
    proposed_precise_type = UnionType.make_union(
        [type_range.item for type_range in proposed_type_ranges if not type_range.is_upper_bound]
    )
    remaining_type = restrict_subtype_away(
        current_type,
        proposed_precise_type,
        consider_runtime_isinstance=consider_runtime_isinstance,
    )

    # Avoid widening the type
    if is_proper_subtype(p_current_type, proposed_type, ignore_promotions=True):
        proposed_type = default if default is not None else current_type

    return proposed_type, remaining_type

