
def ordered_set(*items: _T) -> dict[_T, bool]:
    return dict.fromkeys(items, True)


def ordered_set(*items: T) -> dict[T, Literal[True]]:
    return dict.fromkeys(items, True)

