
def mat_mat_mul(k1, k2):
    """
    Return MatrixKind. The element kind is selected by recursive dispatching.
    """
    elemk = Mul._kind_dispatcher(k1.element_kind, k2.element_kind)
    return MatrixKind(elemk)

