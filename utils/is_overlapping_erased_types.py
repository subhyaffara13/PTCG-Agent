
def is_overlapping_erased_types(
    left: Type, right: Type, *, ignore_promotions: bool = False
) -> bool:
    """The same as 'is_overlapping_erased_types', except the types are erased first."""
    return is_overlapping_types(
        erase_type(left), erase_type(right), ignore_promotions=ignore_promotions
    )

