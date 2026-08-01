
def test_implicit_conversion():
    assert str(m.ClassWithUnscopedEnum.EMode.EFirstMode) == "EMode.EFirstMode"
    assert str(m.ClassWithUnscopedEnum.EFirstMode) == "EMode.EFirstMode"
    assert repr(m.ClassWithUnscopedEnum.EMode.EFirstMode) == "<EMode.EFirstMode: 1>"
    assert repr(m.ClassWithUnscopedEnum.EFirstMode) == "<EMode.EFirstMode: 1>"

    f = m.ClassWithUnscopedEnum.test_function
    first = m.ClassWithUnscopedEnum.EFirstMode
    second = m.ClassWithUnscopedEnum.ESecondMode

    assert f(first) == 1

    assert f(first) == f(first)
    assert not f(first) != f(first)

    assert f(first) != f(second)
    assert not f(first) == f(second)

    assert f(first) == int(f(first))
    assert not f(first) != int(f(first))

    assert f(first) != int(f(second))
    assert not f(first) == int(f(second))

    # noinspection PyDictCreation
    x = {f(first): 1, f(second): 2}
    x[f(first)] = 3
    x[f(second)] = 4
    # Hashing test
    assert repr(x) == "{<EMode.EFirstMode: 1>: 3, <EMode.ESecondMode: 2>: 4}"


def test_implicit_conversion():
    a = Thread(m.test)
    b = Thread(m.test)
    c = Thread(m.test)
    for x in [a, b, c]:
        x.start()
    for x in [c, b, a]:
        x.join()

