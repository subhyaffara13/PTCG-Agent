
def logical_divide(layoutA: Layout, layoutB: LayoutInput) -> Layout:
    if layoutB is None:
        return layoutA
    elif is_int(layoutB):
        return logical_divide(layoutA, Layout(layoutB))
    elif is_tuple(layoutB):
        if len(layoutA) < len(layoutB):
            raise AssertionError
        return make_layout(
            # pyrefly: ignore [bad-argument-type]
            chain(
                (
                    logical_divide(layoutA[i], layoutB[i])  # type: ignore[arg-type]
                    for i in range(len(layoutB))
                ),
                (layoutA[i] for i in range(len(layoutB), len(layoutA))),
            )
        )

    return composition(
        layoutA,
        make_layout(layoutB, complement(layoutB, size(layoutA))),
    )

