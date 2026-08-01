
def test_len():
    assert len(Matrix()) == 0
    assert len(Matrix([[1, 2]])) == len(Matrix([[1], [2]])) == 2
    assert len(Matrix(0, 2, lambda i, j: 0)) == \
        len(Matrix(2, 0, lambda i, j: 0)) == 0
    assert len(Matrix([[0, 1, 2], [3, 4, 5]])) == 6
    assert Matrix([1]) == Matrix([[1]])
    assert not Matrix()
    assert Matrix() == Matrix([])


def test_len():
    assert len(Matrix()) == 0
    assert len(Matrix([[1, 2]])) == len(Matrix([[1], [2]])) == 2
    assert len(Matrix(0, 2, lambda i, j: 0)) == \
        len(Matrix(2, 0, lambda i, j: 0)) == 0
    assert len(Matrix([[0, 1, 2], [3, 4, 5]])) == 6
    assert Matrix([1]) == Matrix([[1]])
    assert not Matrix()
    assert Matrix() == Matrix([])


def test_len():
    assert not SparseMatrix()
    assert SparseMatrix() == SparseMatrix([])
    assert SparseMatrix() == SparseMatrix([[]])


def test_len():
    e = x*y
    assert len(e.args) == 2
    e = x + y + z
    assert len(e.args) == 3


def test_len():
    n = 10
    elements = get_elements(n)
    dis = DisjointSet(elements)
    assert len(dis) == n

    dis.add("dummy")
    assert len(dis) == n + 1


def test_len():
    with pytest.raises(TypeError, match="object of type 'Expression' has no len()"):
        len(pd.col("a"))


def test_len():
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    grouped = df.groupby([lambda x: x.year, lambda x: x.month, lambda x: x.day])
    assert len(grouped) == len(df)

    grouped = df.groupby([lambda x: x.year, lambda x: x.month])
    expected = len({(x.year, x.month) for x in df.index})
    assert len(grouped) == expected


def test_len(any_string_dtype):
    ser = Series(
        ["foo", "fooo", "fooooo", np.nan, "fooooooo", "foo\n", "あ"],
        dtype=any_string_dtype,
    )
    result = ser.str.len()
    if is_object_or_nan_string_dtype(any_string_dtype):
        expected_dtype = "float64"
        item = np.nan
    else:
        expected_dtype = "Int64"
        item = NA
    expected = Series([3, 4, 6, item, 8, 4, 1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

