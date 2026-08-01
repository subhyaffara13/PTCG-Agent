
def _transform_op_ket(a, b):
    return (InnerProduct(a.bra, b), a.ket)

