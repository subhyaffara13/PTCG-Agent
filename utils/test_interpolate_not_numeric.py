
def test_interpolate_not_numeric(data):
    if not data.dtype._is_numeric:
        ser = pd.Series(data)
        msg = re.escape(f"Cannot interpolate with {ser.dtype} dtype")
        with pytest.raises(TypeError, match=msg):
            pd.Series(data).interpolate()

