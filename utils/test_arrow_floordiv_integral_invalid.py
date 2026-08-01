
def test_arrow_floordiv_integral_invalid(pa_type):
    # GH 56676
    min_value = np.iinfo(pa_type.to_pandas_dtype()).min
    a = pd.Series([min_value], dtype=ArrowDtype(pa_type))
    with pytest.raises(pa.lib.ArrowInvalid, match="overflow|not in range"):
        a // -1
    with pytest.raises(pa.lib.ArrowInvalid, match="divide by zero"):
        a // 0

