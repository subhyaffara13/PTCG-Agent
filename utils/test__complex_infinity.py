
def test_ComplexInfinity():
    assert str(zoo) == "zoo"


def test_ComplexInfinity():
    assert zoo.floor() is zoo
    assert zoo.ceiling() is zoo
    assert zoo**zoo is S.NaN

