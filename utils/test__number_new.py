
def test_Number_new():
    """"
    Test for Number constructor
    """
    # Expected behavior on numbers and strings
    assert Number(1) is S.One
    assert Number(2).__class__ is Integer
    assert Number(-622).__class__ is Integer
    assert Number(5, 3).__class__ is Rational
    assert Number(5.3).__class__ is Float
    assert Number('1') is S.One
    assert Number('2').__class__ is Integer
    assert Number('-622').__class__ is Integer
    assert Number('5/3').__class__ is Rational
    assert Number('5.3').__class__ is Float
    raises(ValueError, lambda: Number('cos'))
    raises(TypeError, lambda: Number(cos))
    a = Rational(3, 5)
    assert Number(a) is a  # Check idempotence on Numbers
    u = ['inf', '-inf', 'nan', 'iNF', '+inf']
    v = [oo, -oo, nan, oo, oo]
    for i, a in zip(u, v):
        assert Number(i) is a, (i, Number(i), a)

