
def tiled_divide(layoutA: Layout, layoutB: LayoutInput) -> Layout:
    result = zipped_divide(layoutA, layoutB)
    return make_layout([result[0]] + [result[1][i] for i in range(len(result[1]))])  # type: ignore[arg-type]

