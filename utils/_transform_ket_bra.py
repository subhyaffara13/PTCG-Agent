
def _transform_ket_bra(a, b):
    """Transform a keT*bra -> OuterProduct(ket, bra)."""
    return (OuterProduct(a, b),)

