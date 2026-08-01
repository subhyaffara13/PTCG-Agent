
def test_NegativeInfinity():
    assert str(-oo) == "-oo"


def test_NegativeInfinity():
    assert (-oo).floor() is -oo
    assert (-oo).ceiling() is -oo
    assert (-oo)**11 is -oo
    assert (-oo)**12 is oo

