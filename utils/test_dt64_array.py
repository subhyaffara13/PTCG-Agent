
def test_dt64_array(dtype_unit):
    # GH#53817
    dtype_var = np.dtype(dtype_unit)
    msg = (
        r"datetime64 and timedelta64 dtype resolutions other than "
        r"'s', 'ms', 'us', and 'ns' are no longer supported."
    )
    with pytest.raises(ValueError, match=msg):
        pd.array([], dtype=dtype_var)

