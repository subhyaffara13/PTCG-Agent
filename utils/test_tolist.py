
def test_tolist():
    lst = [[S.One, S.Half, x*y, S.Zero], [x, y, z, x**2], [y, -S.One, z*x, 3]]
    flat_lst = [S.One, S.Half, x*y, S.Zero, x, y, z, x**2, y, -S.One, z*x, 3]
    m = ShapingOnlyMatrix(3, 4, flat_lst)
    assert m.tolist() == lst


def test_tolist():
    lst = [[S.One, S.Half, x*y, S.Zero], [x, y, z, x**2], [y, -S.One, z*x, 3]]
    m = Matrix(lst)
    assert m.tolist() == lst


def test_tolist():
    lst = [[S.One, S.Half, x*y, S.Zero], [x, y, z, x**2], [y, -S.One, z*x, 3]]
    flat_lst = [S.One, S.Half, x*y, S.Zero, x, y, z, x**2, y, -S.One, z*x, 3]
    m = Matrix(3, 4, flat_lst)
    assert m.tolist() == lst


def test_tolist(data):
    result = data.tolist()
    expected = list(data)
    tm.assert_equal(result, expected)


def test_tolist(dtype):
    vals = ["a", "b", "c"]
    arr = pd.array(vals, dtype=dtype)
    result = arr.tolist()
    expected = vals
    tm.assert_equal(result, expected)

