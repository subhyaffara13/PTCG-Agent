
def test_bool(doc):
    assert doc(m.get_bool) == "get_bool() -> bool"


def test_bool():
    assert Eq(0, 0) is S.true
    assert Eq(1, 0) is S.false
    assert Ne(0, 0) is S.false
    assert Ne(1, 0) is S.true
    assert Lt(0, 1) is S.true
    assert Lt(1, 0) is S.false
    assert Le(0, 1) is S.true
    assert Le(1, 0) is S.false
    assert Le(0, 0) is S.true
    assert Gt(1, 0) is S.true
    assert Gt(0, 1) is S.false
    assert Ge(1, 0) is S.true
    assert Ge(0, 1) is S.false
    assert Ge(1, 1) is S.true
    assert Eq(I, 2) is S.false
    assert Ne(I, 2) is S.true
    raises(TypeError, lambda: Gt(I, 2))
    raises(TypeError, lambda: Ge(I, 2))
    raises(TypeError, lambda: Lt(I, 2))
    raises(TypeError, lambda: Le(I, 2))
    a = Float('.000000000000000000001', '')
    b = Float('.0000000000000000000001', '')
    assert Eq(pi + a, pi + b) is S.false


def test_bool():
    with pytest.raises(TypeError, match="boolean value of an expression is ambiguous"):
        bool(pd.col("a"))


def test_bool():
    # Simple test for bool via integer
    txt = StringIO("1, 0\n10, -1")
    res = np.loadtxt(txt, dtype=bool, delimiter=",")
    assert res.dtype == bool
    assert_array_equal(res, [[True, False], [True, True]])
    # Make sure we use only 1 and 0 on the byte level:
    assert_array_equal(res.view(np.uint8), [[1, 0], [1, 1]])

