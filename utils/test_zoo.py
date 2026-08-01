
def test_zoo():
    zoo = S.ComplexInfinity
    assert zoo.is_complex is False
    assert zoo.is_real is False
    assert zoo.is_prime is False


def test_zoo():
    b = Symbol('b', finite=True)
    nz = Symbol('nz', nonzero=True)
    p = Symbol('p', positive=True)
    n = Symbol('n', negative=True)
    im = Symbol('i', imaginary=True)
    c = Symbol('c', complex=True)
    pb = Symbol('pb', positive=True)
    nb = Symbol('nb', negative=True)
    imb = Symbol('ib', imaginary=True, finite=True)
    for i in [I, S.Infinity, S.NegativeInfinity, S.Zero, S.One, S.Pi, S.Half, S(3), log(3),
              b, nz, p, n, im, pb, nb, imb, c]:
        if i.is_finite and (i.is_real or i.is_imaginary):
            assert i + zoo is zoo
            assert i - zoo is zoo
            assert zoo + i is zoo
            assert zoo - i is zoo
        elif i.is_finite is not False:
            assert (i + zoo).is_Add
            assert (i - zoo).is_Add
            assert (zoo + i).is_Add
            assert (zoo - i).is_Add
        else:
            assert (i + zoo) is S.NaN
            assert (i - zoo) is S.NaN
            assert (zoo + i) is S.NaN
            assert (zoo - i) is S.NaN

        if fuzzy_not(i.is_zero) and (i.is_extended_real or i.is_imaginary):
            assert i*zoo is zoo
            assert zoo*i is zoo
        elif i.is_zero:
            assert i*zoo is S.NaN
            assert zoo*i is S.NaN
        else:
            assert (i*zoo).is_Mul
            assert (zoo*i).is_Mul

        if fuzzy_not((1/i).is_zero) and (i.is_real or i.is_imaginary):
            assert zoo/i is zoo
        elif (1/i).is_zero:
            assert zoo/i is S.NaN
        elif i.is_zero:
            assert zoo/i is zoo
        else:
            assert (zoo/i).is_Mul

    assert (I*oo).is_Mul  # allow directed infinity
    assert zoo + zoo is S.NaN
    assert zoo * zoo is zoo
    assert zoo - zoo is S.NaN
    assert zoo/zoo is S.NaN
    assert zoo**zoo is S.NaN
    assert zoo**0 is S.One
    assert zoo**2 is zoo
    assert 1/zoo is S.Zero

    assert Mul.flatten([S.NegativeOne, oo, S(0)]) == ([S.NaN], [], None)

