
def test_Range_symbolic():
    # symbolic Range
    xr = Range(x, x + 4, 5)
    sr = Range(x, y, t)
    i = Symbol('i', integer=True)
    ip = Symbol('i', integer=True, positive=True)
    ipr = Range(ip)
    inr = Range(0, -ip, -1)
    ir = Range(i, i + 19, 2)
    ir2 = Range(i, i*8, 3*i)
    i = Symbol('i', integer=True)
    inf = symbols('inf', infinite=True)
    raises(ValueError, lambda: Range(inf))
    raises(ValueError, lambda: Range(inf, 0, -1))
    raises(ValueError, lambda: Range(inf, inf, 1))
    raises(ValueError, lambda: Range(1, 1, inf))
    # args
    assert xr.args == (x, x + 5, 5)
    assert sr.args == (x, y, t)
    assert ir.args == (i, i + 20, 2)
    assert ir2.args == (i, 10*i, 3*i)
    # reversed
    raises(ValueError, lambda: xr.reversed)
    raises(ValueError, lambda: sr.reversed)
    assert ipr.reversed.args == (ip - 1, -1, -1)
    assert inr.reversed.args == (-ip + 1, 1, 1)
    assert ir.reversed.args == (i + 18, i - 2, -2)
    assert ir2.reversed.args == (7*i, -2*i, -3*i)
    # contains
    assert inf not in sr
    assert inf not in ir
    assert 0 in ipr
    assert 0 in inr
    raises(TypeError, lambda: 1 in ipr)
    raises(TypeError, lambda: -1 in inr)
    assert .1 not in sr
    assert .1 not in ir
    assert i + 1 not in ir
    assert i + 2 in ir
    raises(TypeError, lambda: x in xr)  # XXX is this what contains is supposed to do?
    raises(TypeError, lambda: 1 in sr)  # XXX is this what contains is supposed to do?
    # iter
    raises(ValueError, lambda: next(iter(xr)))
    raises(ValueError, lambda: next(iter(sr)))
    assert next(iter(ir)) == i
    assert next(iter(ir2)) == i
    assert sr.intersect(S.Integers) == sr
    assert sr.intersect(FiniteSet(x)) == Intersection({x}, sr)
    raises(ValueError, lambda: sr[:2])
    raises(ValueError, lambda: xr[0])
    raises(ValueError, lambda: sr[0])
    # len
    assert len(ir) == ir.size == 10
    assert len(ir2) == ir2.size == 3
    raises(ValueError, lambda: len(xr))
    raises(ValueError, lambda: xr.size)
    raises(ValueError, lambda: len(sr))
    raises(ValueError, lambda: sr.size)
    # bool
    assert bool(Range(0)) == False
    assert bool(xr)
    assert bool(ir)
    assert bool(ipr)
    assert bool(inr)
    raises(ValueError, lambda: bool(sr))
    raises(ValueError, lambda: bool(ir2))
    # inf
    raises(ValueError, lambda: xr.inf)
    raises(ValueError, lambda: sr.inf)
    assert ipr.inf == 0
    assert inr.inf == -ip + 1
    assert ir.inf == i
    raises(ValueError, lambda: ir2.inf)
    # sup
    raises(ValueError, lambda: xr.sup)
    raises(ValueError, lambda: sr.sup)
    assert ipr.sup == ip - 1
    assert inr.sup == 0
    assert ir.inf == i
    raises(ValueError, lambda: ir2.sup)
    # getitem
    raises(ValueError, lambda: xr[0])
    raises(ValueError, lambda: sr[0])
    raises(ValueError, lambda: sr[-1])
    raises(ValueError, lambda: sr[:2])
    assert ir[:2] == Range(i, i + 4, 2)
    assert ir[0] == i
    assert ir[-2] == i + 16
    assert ir[-1] == i + 18
    assert ir2[:2] == Range(i, 7*i, 3*i)
    assert ir2[0] == i
    assert ir2[-2] == 4*i
    assert ir2[-1] == 7*i
    raises(ValueError, lambda: Range(i)[-1])
    assert ipr[0] == ipr.inf == 0
    assert ipr[-1] == ipr.sup == ip - 1
    assert inr[0] == inr.sup == 0
    assert inr[-1] == inr.inf == -ip + 1
    raises(ValueError, lambda: ipr[-2])
    assert ir.inf == i
    assert ir.sup == i + 18
    raises(ValueError, lambda: Range(i).inf)
    # as_relational
    assert ir.as_relational(x) == ((x >= i) & (x <= i + 18) &
        Eq(Mod(-i + x, 2), 0))
    assert ir2.as_relational(x) == Eq(
        Mod(-i + x, 3*i), 0) & (((x >= i) & (x <= 7*i) & (3*i >= 1)) |
        ((x <= i) & (x >= 7*i) & (3*i <= -1)))
    assert Range(i, i + 1).as_relational(x) == Eq(x, i)
    assert sr.as_relational(z) == Eq(
        Mod(t, 1), 0) & Eq(Mod(x, 1), 0) & Eq(Mod(-x + z, t), 0
        ) & (((z >= x) & (z <= -t + y) & (t >= 1)) |
        ((z <= x) & (z >= -t + y) & (t <= -1)))
    assert xr.as_relational(z) == Eq(z, x) & Eq(Mod(x, 1), 0)
    # symbols can clash if user wants (but it must be integer)
    assert xr.as_relational(x) == Eq(Mod(x, 1), 0)
    # contains() for symbolic values (issue #18146)
    e = Symbol('e', integer=True, even=True)
    o = Symbol('o', integer=True, odd=True)
    assert Range(5).contains(i) == And(i >= 0, i <= 4)
    assert Range(1).contains(i) == Eq(i, 0)
    assert Range(-oo, 5, 1).contains(i) == (i <= 4)
    assert Range(-oo, oo).contains(i) == True
    assert Range(0, 8, 2).contains(i) == Contains(i, Range(0, 8, 2))
    assert Range(0, 8, 2).contains(e) == And(e >= 0, e <= 6)
    assert Range(0, 8, 2).contains(2*i) == And(2*i >= 0, 2*i <= 6)
    assert Range(0, 8, 2).contains(o) == False
    assert Range(1, 9, 2).contains(e) == False
    assert Range(1, 9, 2).contains(o) == And(o >= 1, o <= 7)
    assert Range(8, 0, -2).contains(o) == False
    assert Range(9, 1, -2).contains(o) == And(o >= 3, o <= 9)
    assert Range(-oo, 8, 2).contains(i) == Contains(i, Range(-oo, 8, 2))

