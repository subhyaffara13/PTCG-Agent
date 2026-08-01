
def test_contract_metric1():
    D = Symbol('D')
    Lorentz = TensorIndexType('Lorentz', dim=D, dummy_name='L')
    a, b, c, d, e = tensor_indices('a,b,c,d,e', Lorentz)
    g = Lorentz.metric
    p = TensorHead('p', [Lorentz])
    t = g(a, b)*p(-b)
    t1 = t.contract_metric(g)
    assert t1 == p(a)
    A, B = tensor_heads('A,B', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))

    # case with g with all free indices
    t1 = A(a,b)*B(-b,c)*g(d, e)
    t2 = t1.contract_metric(g)
    assert t1 == t2

    # case of g(d, -d)
    t1 = A(a,b)*B(-b,c)*g(-d, d)
    t2 = t1.contract_metric(g)
    assert t2 == D*A(a, d)*B(-d, c)

    # g with one free index
    t1 = A(a,b)*B(-b,-c)*g(c, d)
    t2 = t1.contract_metric(g)
    assert t2 == A(a, c)*B(-c, d)

    # g with both indices contracted with another tensor
    t1 = A(a,b)*B(-b,-c)*g(c, -a)
    t2 = t1.contract_metric(g)
    assert _is_equal(t2, A(a, b)*B(-b, -a))

    t1 = A(a,b)*B(-b,-c)*g(c, d)*g(-a, -d)
    t2 = t1.contract_metric(g)
    assert _is_equal(t2, A(a,b)*B(-b,-a))

    t1 = A(a,b)*g(-a,-b)
    t2 = t1.contract_metric(g)
    assert _is_equal(t2, A(a, -a))
    assert not t2.free
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b = tensor_indices('a,b', Lorentz)
    g = Lorentz.metric
    assert _is_equal(g(a, -a).contract_metric(g), Lorentz.dim) # no dim

