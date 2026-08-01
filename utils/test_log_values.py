
def test_log_values():
    assert log(nan) is nan

    assert log(oo) is oo
    assert log(-oo) is oo

    assert log(zoo) is zoo
    assert log(-zoo) is zoo

    assert log(0) is zoo

    assert log(1) == 0
    assert log(-1) == I*pi

    assert log(E) == 1
    assert log(-E).expand() == 1 + I*pi

    assert unchanged(log, pi)
    assert log(-pi).expand() == log(pi) + I*pi

    assert unchanged(log, 17)
    assert log(-17) == log(17) + I*pi

    assert log(I) == I*pi/2
    assert log(-I) == -I*pi/2

    assert log(17*I) == I*pi/2 + log(17)
    assert log(-17*I).expand() == -I*pi/2 + log(17)

    assert log(oo*I) is oo
    assert log(-oo*I) is oo
    assert log(0, 2) is zoo
    assert log(0, 5) is zoo

    assert exp(-log(3))**(-1) == 3

    assert log(S.Half) == -log(2)
    assert log(2*3).func is log
    assert log(2*3**2).func is log

