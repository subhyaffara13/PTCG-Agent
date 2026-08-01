
def logical_product(layoutA: Layout, layoutB: LayoutInput) -> Layout:
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
                    logical_product(layoutA[i], layoutB[i])  # type: ignore[arg-type]
                    for i in range(len(layoutB))
                ),
                (layoutA[i] for i in range(len(layoutB), len(layoutA))),
            )
        )

    return make_layout(
        layoutA,
        composition(complement(layoutA, size(layoutA) * cosize(layoutB)), layoutB),
    )

