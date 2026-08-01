
def test_iter():
    with pytest.raises(TypeError, match="Expression objects are not iterable"):
        iter(pd.col("a"))


def test_iter(idx):
    result = list(idx)
    expected = [
        ("foo", "one"),
        ("foo", "two"),
        ("bar", "one"),
        ("baz", "two"),
        ("qux", "one"),
        ("qux", "two"),
    ]
    assert result == expected

