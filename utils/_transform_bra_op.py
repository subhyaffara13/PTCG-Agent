
def _transform_bra_op(a, b):
    return (InnerProduct(a, b.ket), b.bra)

