
def test_TensAdd_matching():
    """
    Test match and replace with the pattern being a TensAdd
    """
    R3 = TensorIndexType('R3', dim=3)
    p, q = tensor_indices("p q", R3)
    K = TensorHead("K", [R3])
    V = TensorHead("V", [R3])
    W = WildTensorHead('W', unordered_indices=True)

    assert ( K(p)*K(q) + V(p)*V(q) ).matches( K(p)*K(q) + V(p)*V(q) ) == {}
    assert ( K(p)*K(q) + V(p)*V(q) ).matches( K(p)*K(q) + V(p)*V(q) + K(p)*V(q) + V(p)*K(q) ) is None
    assert ( K(p)*K(q) + V(p)*V(q) + K(p)*V(q) + K(q)*V(p) ).replace(
        W(p,q) + K(p)*K(q) + V(p)*V(q),
        W(p,q) + 3*K(p)*V(q)
        ).doit() == K(q)*V(p) + 4*K(p)*V(q)

