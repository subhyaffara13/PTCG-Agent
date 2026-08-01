
def test_relational_assumptions():
    m1 = Symbol("m1", nonnegative=False)
    m2 = Symbol("m2", positive=False)
    m3 = Symbol("m3", nonpositive=False)
    m4 = Symbol("m4", negative=False)
    assert (m1 < 0) == Lt(m1, 0)
    assert (m2 <= 0) == Le(m2, 0)
    assert (m3 > 0) == Gt(m3, 0)
    assert (m4 >= 0) == Ge(m4, 0)
    m1 = Symbol("m1", nonnegative=False, real=True)
    m2 = Symbol("m2", positive=False, real=True)
    m3 = Symbol("m3", nonpositive=False, real=True)
    m4 = Symbol("m4", negative=False, real=True)
    assert (m1 < 0) is S.true
    assert (m2 <= 0) is S.true
    assert (m3 > 0) is S.true
    assert (m4 >= 0) is S.true
    m1 = Symbol("m1", negative=True)
    m2 = Symbol("m2", nonpositive=True)
    m3 = Symbol("m3", positive=True)
    m4 = Symbol("m4", nonnegative=True)
    assert (m1 < 0) is S.true
    assert (m2 <= 0) is S.true
    assert (m3 > 0) is S.true
    assert (m4 >= 0) is S.true
    m1 = Symbol("m1", negative=False, real=True)
    m2 = Symbol("m2", nonpositive=False, real=True)
    m3 = Symbol("m3", positive=False, real=True)
    m4 = Symbol("m4", nonnegative=False, real=True)
    assert (m1 < 0) is S.false
    assert (m2 <= 0) is S.false
    assert (m3 > 0) is S.false
    assert (m4 >= 0) is S.false

