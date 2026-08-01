
def test_evalf_with_zoo():
    assert (1/x).evalf(subs={x: 0}) == zoo  # issue 8242
    assert (-1/x).evalf(subs={x: 0}) == zoo  # PR 16150
    assert (0 ** x).evalf(subs={x: -1}) == zoo  # PR 16150
    assert (0 ** x).evalf(subs={x: -1 + I}) == nan
    assert Mul(2, Pow(0, -1, evaluate=False), evaluate=False).evalf() == zoo  # issue 21147
    assert Mul(x, 1/x, evaluate=False).evalf(subs={x: 0}) == Mul(x, 1/x, evaluate=False).subs(x, 0) == nan
    assert Mul(1/x, 1/x, evaluate=False).evalf(subs={x: 0}) == zoo
    assert Mul(1/x, Abs(1/x), evaluate=False).evalf(subs={x: 0}) == zoo
    assert Abs(zoo, evaluate=False).evalf() == oo
    assert re(zoo, evaluate=False).evalf() == nan
    assert im(zoo, evaluate=False).evalf() == nan
    assert Add(zoo, zoo, evaluate=False).evalf() == nan
    assert Add(oo, zoo, evaluate=False).evalf() == nan
    assert Pow(zoo, -1, evaluate=False).evalf() == 0
    assert Pow(zoo, Rational(-1, 3), evaluate=False).evalf() == 0
    assert Pow(zoo, Rational(1, 3), evaluate=False).evalf() == zoo
    assert Pow(zoo, S.Half, evaluate=False).evalf() == zoo
    assert Pow(zoo, 2, evaluate=False).evalf() == zoo
    assert Pow(0, zoo, evaluate=False).evalf() == nan
    assert log(zoo, evaluate=False).evalf() == zoo
    assert zoo.evalf(chop=True) == zoo
    assert x.evalf(subs={x: zoo}) == zoo

