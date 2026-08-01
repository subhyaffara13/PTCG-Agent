
def _transform_bra_ket(a, b):
    """Transform a bra*ket -> InnerProduct(bra, ket)."""
    return (InnerProduct(a, b),)

