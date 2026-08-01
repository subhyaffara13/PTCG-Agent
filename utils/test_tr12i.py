
def test_TR12i():
    ta, tb, tc = [tan(i) for i in (a, b, c)]
    assert TR12i((ta + tb)/(-ta*tb + 1)) == tan(a + b)
    assert TR12i((ta + tb)/(ta*tb - 1)) == -tan(a + b)
    assert TR12i((-ta - tb)/(ta*tb - 1)) == tan(a + b)
    eq = (ta + tb)/(-ta*tb + 1)**2*(-3*ta - 3*tc)/(2*(ta*tc - 1))
    assert TR12i(eq.expand()) == \
        -3*tan(a + b)*tan(a + c)/(tan(a) + tan(b) - 1)/2
    assert TR12i(tan(x)/sin(x)) == tan(x)/sin(x)
    eq = (ta + cos(2))/(-ta*tb + 1)
    assert TR12i(eq) == eq
    eq = (ta + tb + 2)**2/(-ta*tb + 1)
    assert TR12i(eq) == eq
    eq = ta/(-ta*tb + 1)
    assert TR12i(eq) == eq
    eq = (((ta + tb)*(a + 1)).expand())**2/(ta*tb - 1)
    assert TR12i(eq) == -(a + 1)**2*tan(a + b)

