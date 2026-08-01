
def _transform_op_op(a, b):
    """Extract an inner produt from a product of outer products."""
    return (InnerProduct(a.bra, b.ket), OuterProduct(a.ket, b.bra))

