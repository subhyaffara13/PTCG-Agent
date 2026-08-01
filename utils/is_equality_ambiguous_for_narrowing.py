
def is_equality_ambiguous_for_narrowing(left: Type, right: Type) -> bool:
    """Can left compare equal to right through a value domain outside nominal overlap?"""
    left_info = equality_value_info(left)
    right_info = equality_value_info(right)

    if left_info.is_top or right_info.is_top:
        # Only open-domain enum values can make a top-like type ambiguous.
        # Closed domains can be narrowed to their complete known set instead.
        other_info = right_info if left_info.is_top else left_info
        return any(
            domain in OPEN_VALUE_EQUALITY_DOMAIN_NAMES and domain_info.enum_type_names
            for domain, domain_info in other_info.domains.items()
        )

    shared_domains = left_info.domains.keys() & right_info.domains.keys()
    if not shared_domains:
        return False

    for domain in shared_domains:
        left_domain = left_info.domains[domain]
        right_domain = right_info.domains[domain]
        # Equality between two values from the same enum can still narrow by literal member.
        if (
            left_domain.enum_type_names
            and left_domain.enum_type_names == right_domain.enum_type_names
            and left_domain.type_names == left_domain.enum_type_names
            and right_domain.type_names == right_domain.enum_type_names
        ):
            continue
        # Different domain-member types may compare equal, but nominal narrowing would
        # otherwise treat them as disjoint.
        if left_domain.type_names != right_domain.type_names:
            return True
        # Same domain-member types are only ambiguous if an enum value may compare equal to
        # its underlying value type.
        if left_domain.enum_type_names or right_domain.enum_type_names:
            return True

    return False

