
def left_inverse(layout: LayoutOrIntTuple | None) -> Layout | None:
    if layout is None:
        return None
    elif is_int(layout):
        return Layout(layout)
    return right_inverse(make_layout(complement(layout), layout))  # type: ignore[arg-type]

