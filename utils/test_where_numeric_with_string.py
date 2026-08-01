
def test_where_numeric_with_string():
    # GH 9280
    s = Series([1, 2, 3])
    w = s.where(s > 1, "X")

    assert not is_integer(w[0])
    assert is_integer(w[1])
    assert is_integer(w[2])
    assert isinstance(w[0], str)
    assert w.dtype == "object"

    w = s.where(s > 1, ["X", "Y", "Z"])
    assert not is_integer(w[0])
    assert is_integer(w[1])
    assert is_integer(w[2])
    assert isinstance(w[0], str)
    assert w.dtype == "object"

    w = s.where(s > 1, np.array(["X", "Y", "Z"]))
    assert not is_integer(w[0])
    assert is_integer(w[1])
    assert is_integer(w[2])
    assert isinstance(w[0], str)
    assert w.dtype == "object"

