
def test_fun():
    with warns_deprecated_sympy():
        D = Symbol('D')
        Lorentz = TensorIndexType('Lorentz', dim=D, dummy_name='L')
        a, b, c, d, e = tensor_indices('a,b,c,d,e', Lorentz)
        g = Lorentz.metric

        p, q = tensor_heads('p q', [Lorentz])
        t = q(c)*p(a)*q(b) + g(a,b)*g(c,d)*q(-d)
        assert t(a,b,c) == t
        assert canon_bp(t - t(b,a,c) - q(c)*p(a)*q(b) + q(c)*p(b)*q(a)) == 0
        assert t(b,c,d) == q(d)*p(b)*q(c) + g(b,c)*g(d,e)*q(-e)
        t1 = t.substitute_indices((a,b),(b,a))
        assert canon_bp(t1 - q(c)*p(b)*q(a) - g(a,b)*g(c,d)*q(-d)) == 0

        # check that g_{a b; c} = 0
        # example taken from  L. Brewin
        # "A brief introduction to Cadabra" arxiv:0903.2085
        # dg_{a b c} = \partial_{a} g_{b c} is symmetric in b, c
        dg = TensorHead('dg', [Lorentz]*3, TensorSymmetry.direct_product(1, 2))
        # gamma^a_{b c} is the Christoffel symbol
        gamma = S.Half*g(a,d)*(dg(-b,-d,-c) + dg(-c,-b,-d) - dg(-d,-b,-c))
        # t = g_{a b; c}
        t = dg(-c,-a,-b) - g(-a,-d)*gamma(d,-b,-c) - g(-b,-d)*gamma(d,-a,-c)
        t = t.contract_metric(g)
        assert t == 0
        t = q(c)*p(a)*q(b)
        assert t(b,c,d) == q(d)*p(b)*q(c)


def test_fun():
    assert (FiniteSet(*ImageSet(Lambda(x, sin(pi*x/4)),
        Range(-10, 11))) == FiniteSet(-1, -sqrt(2)/2, 0, sqrt(2)/2, 1))


def test_fun():
    R, x, y = ring('x, y', QQ)
    p = x*y + x**2*y**3 + x**5*y
    assert rs_fun(p, rs_tan, x, 10) == rs_tan(p, x, 10)
    assert rs_fun(p, _tan1, x, 10) == _tan1(p, x, 10)

