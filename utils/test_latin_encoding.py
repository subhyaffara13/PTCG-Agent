
def test_latin_encoding(temp_h5_path, dtype, val):
    enc = "latin-1"
    nan_rep = ""
    key = "data"

    val = [x.decode(enc) if isinstance(x, bytes) else x for x in val]
    ser = Series(val, dtype=dtype)

    ser.to_hdf(temp_h5_path, key=key, format="table", encoding=enc, nan_rep=nan_rep)
    retr = read_hdf(temp_h5_path, key)

    # TODO:(3.0): once Categorical replace deprecation is enforced,
    #  we may be able to re-simplify the construction of s_nan
    if dtype == "category":
        if nan_rep in ser.cat.categories:
            s_nan = ser.cat.remove_categories([nan_rep])
        else:
            s_nan = ser
    else:
        s_nan = ser.replace(nan_rep, np.nan)

    tm.assert_series_equal(s_nan, retr)

