
def num_vec_mul(k1, k2):
    """
    The result of a multiplication between a number and a Vector should be of VectorKind.
    The element kind is selected by recursive dispatching.
    """
    if not isinstance(k2, VectorKind):
        k1, k2 = k2, k1
    elemk = Mul._kind_dispatcher(k1, k2.element_kind)
    return VectorKind(elemk)

