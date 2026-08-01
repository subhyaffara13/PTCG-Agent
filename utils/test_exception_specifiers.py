
def test_exception_specifiers():
    c = m.C()
    assert c.m1(2) == 1
    assert c.m2(3) == 1
    assert c.m3(5) == 2
    assert c.m4(7) == 3
    assert c.m5(10) == 5
    assert c.m6(14) == 8
    assert c.m7(20) == 13
    assert c.m8(29) == 21

    assert m.f1(33) == 34
    assert m.f2(53) == 55
    assert m.f3(86) == 89
    assert m.f4(140) == 144

