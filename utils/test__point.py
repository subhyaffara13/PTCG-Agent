
def test_Point():
    #The curve is of the form y**2 = x**3 + a*x**2 + x
    mod = 101
    a = 10
    a_24 = (a + 2)*invert(4, mod)
    p1 = Point(10, 17, a_24, mod)
    p2 = p1.double()
    assert p2 == Point(68, 56, a_24, mod)
    p4 = p2.double()
    assert p4 == Point(22, 64, a_24, mod)
    p8 = p4.double()
    assert p8 == Point(71, 95, a_24, mod)
    p16 = p8.double()
    assert p16 == Point(5, 16, a_24, mod)
    p32 = p16.double()
    assert p32 == Point(33, 96, a_24, mod)

    # p3 = p2 + p1
    p3 = p2.add(p1, p1)
    assert p3 == Point(1, 61, a_24, mod)
    # p5 = p3 + p2 or p4 + p1
    p5 = p3.add(p2, p1)
    assert p5 == Point(49, 90, a_24, mod)
    assert p5 == p4.add(p1, p3)
    # p6 = 2*p3
    p6 = p3.double()
    assert p6 == Point(87, 43, a_24, mod)
    assert p6 == p4.add(p2, p2)
    # p7 = p5 + p2
    p7 = p5.add(p2, p3)
    assert p7 == Point(69, 23, a_24, mod)
    assert p7 == p4.add(p3, p1)
    assert p7 == p6.add(p1, p5)
    # p9 = p5 + p4
    p9 = p5.add(p4, p1)
    assert p9 == Point(56, 99, a_24, mod)
    assert p9 == p6.add(p3, p3)
    assert p9 == p7.add(p2, p5)
    assert p9 == p8.add(p1, p7)

    assert p5 == p1.mont_ladder(5)
    assert p9 == p1.mont_ladder(9)
    assert p16 == p1.mont_ladder(16)
    assert p9 == p3.mont_ladder(3)

