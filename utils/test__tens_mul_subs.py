
def test_TensMul_subs():
    """
    Test subs and xreplace in TensMul. See bug #24337
    """
    R3 = TensorIndexType('R3', dim=3)
    p, q, r = tensor_indices("p q r", R3)
    K = TensorHead("K", [R3])
    V = TensorHead("V", [R3])
    A = TensorHead("A", [R3, R3])
    C0 = TensorIndex(R3.dummy_name + "_0", R3, True)
    a = WildTensorIndex("a", R3, ignore_updown=True)

    assert ( K(p)*V(r)*K(-p) ).subs({V(r): K(q)*K(-q)}) == K(p)*K(q)*K(-q)*K(-p)
    assert ( K(p)*V(r)*K(-p) ).xreplace({V(r): K(q)*K(-q)}) == K(p)*K(q)*K(-q)*K(-p)
    assert ( K(p)*V(r) ).xreplace({p: C0, V(r): K(q)*K(-q)}) == K(C0)*K(q)*K(-q)
    assert ( K(p)*A(q,-q)*K(-p) ).doit() == K(p)*A(q,-q)*K(-p)
    assert ( K(p)*V(-p) ).replace( K(a), V(a)*V(q)*V(-q) ) == V(p)*V(q)*V(-q)*V(-p)

