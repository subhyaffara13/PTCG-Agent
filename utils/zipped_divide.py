
def zipped_divide(layoutA: Layout, layoutB: LayoutInput) -> Layout:
    return hier_unzip(logical_divide, layoutA, layoutB)

