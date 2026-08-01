
def zipped_product(layoutA: Layout, layoutB: LayoutInput) -> Layout:
    return hier_unzip(logical_product, layoutA, layoutB)

