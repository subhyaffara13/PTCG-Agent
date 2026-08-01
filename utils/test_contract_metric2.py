
def test_contract_metric2():
    D = Symbol('D')
    Lorentz = TensorIndexType('Lorentz', dim=D, dummy_name='L')
    a, b, c, d, e, L_0 = tensor_indices('a,b,c,d,e,L_0', Lorentz)
    g = Lorentz.metric
    p, q = tensor_heads('p,q', [Lorentz])

    t1 = g(a,b)*p(c)*p(-c)
    t2 = 3*g(-a,-b)*q(c)*q(-c)
    t = t1*t2
    t = t.contract_metric(g)
    assert t == 3*D*p(a)*p(-a)*q(b)*q(-b)
    t1 = g(a,b)*p(c)*p(-c)
    t2 = 3*q(-a)*q(-b)
    t = t1*t2
    t = t.contract_metric(g)
    t = t.canon_bp()
    assert t == 3*p(a)*p(-a)*q(b)*q(-b)

    t1 = 2*g(a,b)*p(c)*p(-c)
    t2 = - 3*g(-a,-b)*q(c)*q(-c)
    t = t1*t2
    t = t.contract_metric(g)
    t = 6*g(a,b)*g(-a,-b)*p(c)*p(-c)*q(d)*q(-d)
    t = t.contract_metric(g)

    t1 = 2*g(a,b)*p(c)*p(-c)
    t2 = q(-a)*q(-b) + 3*g(-a,-b)*q(c)*q(-c)
    t = t1*t2
    t = t.contract_metric(g)
    assert t == (2 + 6*D)*p(a)*p(-a)*q(b)*q(-b)

    t1 = p(a)*p(b) + p(a)*q(b) + 2*g(a,b)*p(c)*p(-c)
    t2 = q(-a)*q(-b) - g(-a,-b)*q(c)*q(-c)
    t = t1*t2
    t = t.contract_metric(g)
    t1 = (1 - 2*D)*p(a)*p(-a)*q(b)*q(-b) + p(a)*q(-a)*p(b)*q(-b)
    assert canon_bp(t - t1) == 0

    t = g(a,b)*g(c,d)*g(-b,-c)
    t1 = t.contract_metric(g)
    assert t1 == g(a, d)

    t1 = g(a,b)*g(c,d) + g(a,c)*g(b,d) + g(a,d)*g(b,c)
    t2 = t1.substitute_indices((a,-a),(b,-b),(c,-c),(d,-d))
    t = t1*t2
    t = t.contract_metric(g)
    assert t.equals(3*D**2 + 6*D)

    t = 2*p(a)*g(b,-b)
    t1 = t.contract_metric(g)
    assert t1.equals(2*D*p(a))

    t = 2*p(a)*g(b,-a)
    t1 = t.contract_metric(g)
    assert t1 == 2*p(b)

    M = Symbol('M')
    t = (p(a)*p(b) + g(a, b)*M**2)*g(-a, -b) - D*M**2
    t1 = t.contract_metric(g)
    assert t1 == p(a)*p(-a)

    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(a, b)*p(L_0)*g(-a, -b)
    t1 = t.contract_metric(g)
    assert str(t1) == 'A(L_1, -L_1)*p(L_0)' or str(t1) == 'A(-L_1, L_1)*p(L_0)'

