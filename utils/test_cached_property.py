
def test_cached_property():
    class A:
        def __init__(self, value):
            self.value = value
            self.calls = 0

        @cached_property
        def prop(self):
            self.calls = self.calls + 1
            return self.value

    a = A(2)
    assert a.calls == 0
    assert a.prop == 2
    assert a.calls == 1
    assert a.prop == 2
    assert a.calls == 1
    b = A(None)
    assert b.prop == None


def test_cached_property() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    # Ensure test is valid
    assert isinstance(pd.Index.dtype, cache_readonly)

    df = pd.DataFrame({"a": [1, 2, 3]})
    expr = pd.col("a").index.dtype
    expected_str = "col('a').index.dtype"
    assert str(expr) == expected_str

    result = df.assign(b=expr)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": np.int64})
    tm.assert_frame_equal(result, expected)

