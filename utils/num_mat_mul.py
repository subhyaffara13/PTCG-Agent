
def num_mat_mul(k1, k2):
    """
    Return MatrixKind. The element kind is selected by recursive dispatching.
    Do not need to dispatch in reversed order because KindDispatcher
    searches for this automatically.
    """
    # Deal with Mul._kind_dispatcher's commutativity
    # XXX: this function is called with either k1 or k2 as MatrixKind because
    # the Mul kind dispatcher is commutative. Maybe it shouldn't be. Need to
    # swap the args here because NumberKind does not have an element_kind
    # attribute.
    if not isinstance(k2, MatrixKind):
        k1, k2 = k2, k1
    elemk = Mul._kind_dispatcher(k1, k2.element_kind)
    return MatrixKind(elemk)

