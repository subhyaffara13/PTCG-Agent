
def test_custom_accessor() -> None:
    df = pd.DataFrame({"a": [1, 2, 3]})

    class XYZAccessor:
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def mean(self):
            return self._obj.mean()

    with ensure_removed(pd.Series, "xyz"):
        pd.api.extensions.register_series_accessor("xyz")(XYZAccessor)
        result = df.assign(b=pd.col("a").xyz.mean())
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [2.0, 2.0, 2.0]})
    tm.assert_frame_equal(result, expected)

