
def test_Infinity():
    assert str(oo) == "oo"
    assert str(oo*I) == "oo*I"


def test_Infinity():
    assert oo != 1
    assert 1*oo is oo
    assert 1 != oo
    assert oo != -oo
    assert oo != Symbol("x")**3
    assert oo + 1 is oo
    assert 2 + oo is oo
    assert 3*oo + 2 is oo
    assert S.Half**oo == 0
    assert S.Half**(-oo) is oo
    assert -oo*3 is -oo
    assert oo + oo is oo
    assert -oo + oo*(-5) is -oo
    assert 1/oo == 0
    assert 1/(-oo) == 0
    assert 8/oo == 0
    assert oo % 2 is nan
    assert 2 % oo is nan
    assert oo/oo is nan
    assert oo/-oo is nan
    assert -oo/oo is nan
    assert -oo/-oo is nan
    assert oo - oo is nan
    assert oo - -oo is oo
    assert -oo - oo is -oo
    assert -oo - -oo is nan
    assert oo + -oo is nan
    assert -oo + oo is nan
    assert oo + oo is oo
    assert -oo + oo is nan
    assert oo + -oo is nan
    assert -oo + -oo is -oo
    assert oo*oo is oo
    assert -oo*oo is -oo
    assert oo*-oo is -oo
    assert -oo*-oo is oo
    assert oo/0 is oo
    assert -oo/0 is -oo
    assert 0/oo == 0
    assert 0/-oo == 0
    assert oo*0 is nan
    assert -oo*0 is nan
    assert 0*oo is nan
    assert 0*-oo is nan
    assert oo + 0 is oo
    assert -oo + 0 is -oo
    assert 0 + oo is oo
    assert 0 + -oo is -oo
    assert oo - 0 is oo
    assert -oo - 0 is -oo
    assert 0 - oo is -oo
    assert 0 - -oo is oo
    assert oo/2 is oo
    assert -oo/2 is -oo
    assert oo/-2 is -oo
    assert -oo/-2 is oo
    assert oo*2 is oo
    assert -oo*2 is -oo
    assert oo*-2 is -oo
    assert 2/oo == 0
    assert 2/-oo == 0
    assert -2/oo == 0
    assert -2/-oo == 0
    assert 2*oo is oo
    assert 2*-oo is -oo
    assert -2*oo is -oo
    assert -2*-oo is oo
    assert 2 + oo is oo
    assert 2 - oo is -oo
    assert -2 + oo is oo
    assert -2 - oo is -oo
    assert 2 + -oo is -oo
    assert 2 - -oo is oo
    assert -2 + -oo is -oo
    assert -2 - -oo is oo
    assert S(2) + oo is oo
    assert S(2) - oo is -oo
    assert oo/I == -oo*I
    assert -oo/I == oo*I
    assert oo*float(1) == _inf and (oo*float(1)) is oo
    assert -oo*float(1) == _ninf and (-oo*float(1)) is -oo
    assert oo/float(1) == _inf and (oo/float(1)) is oo
    assert -oo/float(1) == _ninf and (-oo/float(1)) is -oo
    assert oo*float(-1) == _ninf and (oo*float(-1)) is -oo
    assert -oo*float(-1) == _inf and (-oo*float(-1)) is oo
    assert oo/float(-1) == _ninf and (oo/float(-1)) is -oo
    assert -oo/float(-1) == _inf and (-oo/float(-1)) is oo
    assert oo + float(1) == _inf and (oo + float(1)) is oo
    assert -oo + float(1) == _ninf and (-oo + float(1)) is -oo
    assert oo - float(1) == _inf and (oo - float(1)) is oo
    assert -oo - float(1) == _ninf and (-oo - float(1)) is -oo
    assert float(1)*oo == _inf and (float(1)*oo) is oo
    assert float(1)*-oo == _ninf and (float(1)*-oo) is -oo
    assert float(1)/oo == 0
    assert float(1)/-oo == 0
    assert float(-1)*oo == _ninf and (float(-1)*oo) is -oo
    assert float(-1)*-oo == _inf and (float(-1)*-oo) is oo
    assert float(-1)/oo == 0
    assert float(-1)/-oo == 0
    assert float(1) + oo is oo
    assert float(1) + -oo is -oo
    assert float(1) - oo is -oo
    assert float(1) - -oo is oo
    assert oo == float(oo)
    assert (oo != float(oo)) is False
    assert type(float(oo)) is float
    assert -oo == float(-oo)
    assert (-oo != float(-oo)) is False
    assert type(float(-oo)) is float

    assert Float('nan') is nan
    assert nan*1.0 is nan
    assert -1.0*nan is nan
    assert nan*oo is nan
    assert nan*-oo is nan
    assert nan/oo is nan
    assert nan/-oo is nan
    assert nan + oo is nan
    assert nan + -oo is nan
    assert nan - oo is nan
    assert nan - -oo is nan
    assert -oo * S.Zero is nan

    assert oo*nan is nan
    assert -oo*nan is nan
    assert oo/nan is nan
    assert -oo/nan is nan
    assert oo + nan is nan
    assert -oo + nan is nan
    assert oo - nan is nan
    assert -oo - nan is nan
    assert S.Zero * oo is nan
    assert oo.is_Rational is False
    assert isinstance(oo, Rational) is False

    assert S.One/oo == 0
    assert -S.One/oo == 0
    assert S.One/-oo == 0
    assert -S.One/-oo == 0
    assert S.One*oo is oo
    assert -S.One*oo is -oo
    assert S.One*-oo is -oo
    assert -S.One*-oo is oo
    assert S.One/nan is nan
    assert S.One - -oo is oo
    assert S.One + nan is nan
    assert S.One - nan is nan
    assert nan - S.One is nan
    assert nan/S.One is nan
    assert -oo - S.One is -oo

