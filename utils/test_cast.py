
def test_cast():
    vo = m.VectorOwner.Create(0)
    assert m.py_cast_VectorOwner_ptr(vo) is vo


def test_cast(Poly1, Poly2):
    x = np.linspace(0, 1, 10)
    coef = random((3,))

    d1 = Poly1.domain + random((2,)) * .25
    w1 = Poly1.window + random((2,)) * .25
    p1 = Poly1(coef, domain=d1, window=w1)

    d2 = Poly2.domain + random((2,)) * .25
    w2 = Poly2.window + random((2,)) * .25
    p2 = Poly2.cast(p1, domain=d2, window=w2)

    assert_almost_equal(p2.domain, d2)
    assert_almost_equal(p2.window, w2)
    assert_almost_equal(p2(x), p1(x))

