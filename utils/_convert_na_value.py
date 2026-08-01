
def _convert_na_value(ser, expected):
    if ser.dtype != object:
        if ser.dtype.na_value is np.nan:
            expected = expected.fillna(np.nan)
        else:
            # GH#18463
            expected = expected.fillna(pd.NA)
    return expected

