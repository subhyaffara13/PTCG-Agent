
def dict_flatten(
    dct: dict[_KT, _VT], /
) -> tuple[list[_VT], tuple[list[_KT], list[_KT]], tuple[_KT, ...]]:
    sorted_keys = optree.utils.total_order_sorted(dct)
    values = [dct[key] for key in sorted_keys]
    original_keys = list(dct)
    return values, (original_keys, sorted_keys), tuple(sorted_keys)

