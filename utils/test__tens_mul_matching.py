
def test_TensMul_matching():
    """
    Test match and replace with the pattern being a TensMul
    """
    R3 = TensorIndexType('R3', dim=3)
    p, q, r, s, t = tensor_indices("p q r s t", R3)
    wi = Wild("wi")
    a,b,c,d,e,f = symbols("a b c d e f", cls = WildTensorIndex, tensor_index_type=R3, ignore_updown=True)
    delta = R3.delta
    eps = R3.epsilon
    K = TensorHead("K", [R3])
    V = TensorHead("V", [R3])
    W = WildTensorHead('W', unordered_indices=True)
    U = WildTensorHead('U')
    k = Symbol("K")

    assert ( wi*K(p) ).matches( K(p) ) == {wi: 1}
    assert ( wi * eps(p,q,r) ).matches(eps(p,r,q)) == {wi:-1}
    assert ( K(p)*V(-p) ).replace( W(a)*V(-a), 1) == 1
    assert ( K(q)*K(p)*V(-p) ).replace( W(q,a)*V(-a), 1) == 1
    assert ( K(p)*V(-p) ).replace( K(-a)*V(a), 1 ) == 1
    assert ( K(q)*K(p)*V(-p) ).replace( W(q)*U(p)*V(-p), 1) == 1
    assert (
        (K(p)*V(q)).replace(W()*K(p)*V(q), W()*V(p)*V(q)).doit()
        == V(p)*V(q)
        )
    assert (
        ( eps(r,p,q)*eps(-r,-s,-t) ).replace(
            eps(e,a,b)*eps(-e,c,d),
            delta(a,c)*delta(b,d) - delta(a,d)*delta(b,c),
            ).doit().canon_bp()
        == delta(p,-s)*delta(q,-t) - delta(p,-t)*delta(q,-s)
        )
    assert (
        ( eps(r,p,q)*eps(-r,-p,-q) ).replace(
            eps(c,a,b)*eps(-c,d,f),
            delta(a,d)*delta(b,f) - delta(a,f)*delta(b,d),
            ).contract_delta(delta).doit()
        == 6
        )
    assert ( V(-p)*V(q)*V(-q) ).replace( wi*W()*V(a)*V(-a), wi*W() ).doit() == V(-p)
    assert ( k**4*K(r)*K(-r) ).replace( wi*W()*K(a)*K(-a), wi*W()*k**2 ).doit() == k**6

    #Multiple occurrence of WildTensor in value
    assert (
        ( K(p)*V(q) ).replace(W(q)*K(p), W(p)*W(q))
        == V(p)*V(q)
        )
    assert (
        ( K(p)*V(q)*V(r) ).replace(W(q,r)*K(p), W(p,r)*W(q,s)*V(-s) )
        == V(p)*V(r)*V(q)*V(s)*V(-s)
        )

    #Edge case involving automatic index relabelling
    D0, D1, D2, D3 = tensor_indices("R_0 R_1 R_2 R_3", R3)
    expr = delta(-D0, -D1)*K(D2)*K(D3)*K(-D3)
    m = ( W()*K(a)*K(-a) ).matches(expr)
    assert D2 not in m.values()

