
def test_sub():
    per = SeqPer((1, 2), (n, 0, oo))
    form = SeqFormula(n**2)

    assert per - (SeqPer((2, 3))) == SeqPer((-1, -1), (n, 0, oo))
    assert form - (SeqFormula(n**3)) == SeqFormula(n**2 - n**3)

    assert per - form == SeqAdd(per, -form)

    raises(TypeError, lambda: per - n)
    raises(TypeError, lambda: n - per)


def test_sub():
    n = ArithmeticOnlyMatrix(1, 2, [1, 2])
    assert n - n == ArithmeticOnlyMatrix(1, 2, [0, 0])


def test_sub():
    n = Matrix(1, 2, [1, 2])
    assert n - n == Matrix(1, 2, [0, 0])


def test_sub():
    assert h - l == h - x == 1
    assert l - h == x - h == 2
    assert x - l == -(l - x) == x + 1


def test_sub(date, offset_box, offset2):
    off = offset2
    msg = "Cannot subtract datetime from offset"
    with pytest.raises(TypeError, match=msg):
        off - date

    assert 2 * off - off == off
    assert date - offset2 == date + offset_box(-2)
    assert date - offset2 == date - (2 * off - off)


def test_sub(idx):
    first = idx

    # - now raises (previously was set op difference)
    msg = "cannot perform __sub__ with this index type: MultiIndex"
    with pytest.raises(TypeError, match=msg):
        first - idx[-3:]
    with pytest.raises(TypeError, match=msg):
        idx[-3:] - first
    with pytest.raises(TypeError, match=msg):
        idx[-3:] - first.tolist()
    msg = "cannot perform __rsub__ with this index type: MultiIndex"
    with pytest.raises(TypeError, match=msg):
        first.tolist() - idx[-3:]


def test_sub(left_array, right_array):
    msg = (
        r"numpy boolean subtract, the `-` operator, is (?:deprecated|not supported), "
        r"use the bitwise_xor, the `\^` operator, or the logical_xor function instead\."
    )
    with pytest.raises(TypeError, match=msg):
        left_array - right_array


def test_sub(dtype):
    a = pd.array([1, 2, 3, None, 5], dtype=dtype)
    b = pd.array([0, 1, None, 3, 4], dtype=dtype)

    result = a - b
    expected = pd.array([1, 1, None, None, 1], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)


def test_sub(Poly):
    # This checks commutation, not numerical correctness
    c1 = list(random((4,)) + .5)
    c2 = list(random((3,)) + .5)
    p1 = Poly(c1)
    p2 = Poly(c2)
    p3 = p1 - p2
    assert_poly_almost_equal(p2 - p1, -p3)
    assert_poly_almost_equal(p1 - c2, p3)
    assert_poly_almost_equal(c2 - p1, -p3)
    assert_poly_almost_equal(p1 - tuple(c2), p3)
    assert_poly_almost_equal(tuple(c2) - p1, -p3)
    assert_poly_almost_equal(p1 - np.array(c2), p3)
    assert_poly_almost_equal(np.array(c2) - p1, -p3)
    assert_raises(TypeError, op.sub, p1, Poly([0], domain=Poly.domain + 1))
    assert_raises(TypeError, op.sub, p1, Poly([0], window=Poly.window + 1))
    if Poly is Polynomial:
        assert_raises(TypeError, op.sub, p1, Chebyshev([0]))
    else:
        assert_raises(TypeError, op.sub, p1, Polynomial([0]))


def test_sub():
    assert mpf(2.5) - mpf(3) == -0.5
    assert mpf(2.5) - 3 == -0.5
    assert mpf(2.5) - 3.0 == -0.5
    assert 3 - mpf(2.5) == 0.5
    assert 3.0 - mpf(2.5) == 0.5
    assert (3+0j) - mpf(2.5) == 0.5
    assert mpc(2.5) - mpf(3) == -0.5
    assert mpc(2.5) - 3 == -0.5
    assert mpc(2.5) - 3.0 == -0.5
    assert mpc(2.5) - (3+0j) == -0.5
    assert 3 - mpc(2.5) == 0.5
    assert 3.0 - mpc(2.5) == 0.5
    assert (3+0j) - mpc(2.5) == 0.5

