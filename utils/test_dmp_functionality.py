
def test_DMP_functionality():
    f = DMP([[ZZ(1)], [ZZ(2), ZZ(0)], [ZZ(1), ZZ(0), ZZ(0)]], ZZ)
    g = DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)
    h = DMP([[ZZ(1)]], ZZ)

    assert f.degree() == 2
    assert f.degree_list() == (2, 2)
    assert f.total_degree() == 2

    assert f.LC() == ZZ(1)
    assert f.TC() == ZZ(0)
    assert f.nth(1, 1) == ZZ(2)

    raises(TypeError, lambda: f.nth(0, 'x'))

    assert f.max_norm() == 2
    assert f.l1_norm() == 4

    u = DMP([[ZZ(2)], [ZZ(2), ZZ(0)]], ZZ)

    assert f.diff(m=1, j=0) == u
    assert f.diff(m=1, j=1) == u

    raises(TypeError, lambda: f.diff(m='x', j=0))

    u = DMP([ZZ(1), ZZ(2), ZZ(1)], ZZ)
    v = DMP([ZZ(1), ZZ(2), ZZ(1)], ZZ)

    assert f.eval(a=1, j=0) == u
    assert f.eval(a=1, j=1) == v

    assert f.eval(1).eval(1) == ZZ(4)

    assert f.cofactors(g) == (g, g, h)
    assert f.gcd(g) == g
    assert f.lcm(g) == f

    u = DMP([[QQ(45), QQ(30), QQ(5)]], QQ)
    v = DMP([[QQ(1), QQ(2, 3), QQ(1, 9)]], QQ)

    assert u.monic() == v

    assert (4*f).content() == ZZ(4)
    assert (4*f).primitive() == (ZZ(4), f)

    f = DMP([QQ(1,3), QQ(1)], QQ)
    g = DMP([QQ(1,7), QQ(1)], QQ)

    assert f.cancel(g) == f.cancel(g, include=True) == (
        DMP([QQ(7), QQ(21)], QQ),
        DMP([QQ(3), QQ(21)], QQ)
    )
    assert f.cancel(g, include=False) == (
        QQ(7),
        QQ(3),
        DMP([QQ(1), QQ(3)], QQ),
        DMP([QQ(1), QQ(7)], QQ)
    )

    f = DMP([[ZZ(1)], [ZZ(2)], [ZZ(3)], [ZZ(4)], [ZZ(5)], [ZZ(6)]], ZZ)

    assert f.trunc(3) == DMP([[ZZ(1)], [ZZ(-1)], [], [ZZ(1)], [ZZ(-1)], []], ZZ)

    f = DMP(f_4, ZZ)

    assert f.sqf_part() == -f
    assert f.sqf_list() == (ZZ(-1), [(-f, 1)])

    f = DMP([[ZZ(-1)], [], [], [ZZ(5)]], ZZ)
    g = DMP([[ZZ(3), ZZ(1)], [], []], ZZ)
    h = DMP([[ZZ(45), ZZ(30), ZZ(5)]], ZZ)

    r = DMP([ZZ(675), ZZ(675), ZZ(225), ZZ(25)], ZZ)

    assert f.subresultants(g) == [f, g, h]
    assert f.resultant(g) == r

    f = DMP([ZZ(1), ZZ(3), ZZ(9), ZZ(-13)], ZZ)

    assert f.discriminant() == -11664

    f = DMP([QQ(2), QQ(0)], QQ)
    g = DMP([QQ(1), QQ(0), QQ(-16)], QQ)

    s = DMP([QQ(1, 32), QQ(0)], QQ)
    t = DMP([QQ(-1, 16)], QQ)
    h = DMP([QQ(1)], QQ)

    assert f.half_gcdex(g) == (s, h)
    assert f.gcdex(g) == (s, t, h)

    assert f.invert(g) == s

    f = DMP([[QQ(1)], [QQ(2)], [QQ(3)]], QQ)

    raises(ValueError, lambda: f.half_gcdex(f))
    raises(ValueError, lambda: f.gcdex(f))

    raises(ValueError, lambda: f.invert(f))

    f = DMP(ZZ.map([1, 0, 20, 0, 150, 0, 500, 0, 625, -2, 0, -10, 9]), ZZ)
    g = DMP([ZZ(1), ZZ(0), ZZ(0), ZZ(-2), ZZ(9)], ZZ)
    h = DMP([ZZ(1), ZZ(0), ZZ(5), ZZ(0)], ZZ)

    assert g.compose(h) == f
    assert f.decompose() == [g, h]

    f = DMP([[QQ(1)], [QQ(2)], [QQ(3)]], QQ)

    raises(ValueError, lambda: f.decompose())
    raises(ValueError, lambda: f.sturm())

