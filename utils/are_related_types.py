
def are_related_types(
    left: Type, right: Type, *, proper_subtype: bool, ignore_promotions: bool
) -> bool:
    if proper_subtype:
        return is_proper_subtype(
            left, right, ignore_promotions=ignore_promotions
        ) or is_proper_subtype(right, left, ignore_promotions=ignore_promotions)
    else:
        return is_subtype(left, right, ignore_promotions=ignore_promotions) or is_subtype(
            right, left, ignore_promotions=ignore_promotions
        )

