
def is_subset_no_promote(left: Type, right: Type) -> bool:
    return is_subtype(left, right, ignore_promotions=True, always_covariant=True)

