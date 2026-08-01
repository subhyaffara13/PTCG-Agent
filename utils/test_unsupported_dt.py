
def test_unsupported_dt(data):
    pa_dtype = data.dtype.pyarrow_dtype
    if not pa.types.is_temporal(pa_dtype):
        with pytest.raises(
            AttributeError, match="Can only use .dt accessor with datetimelike values"
        ):
            pd.Series(data).dt

