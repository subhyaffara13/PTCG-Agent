
def test_to_hdf_errors(format, temp_h5_path, using_infer_string):
    data = ["\ud800foo"]
    ser = Series(data, index=Index(data, dtype="object"), dtype="object")
    # GH 20835
    ser.to_hdf(temp_h5_path, key="table", format=format, errors="surrogatepass")

    result = read_hdf(temp_h5_path, "table", errors="surrogatepass")

    if using_infer_string:
        # https://github.com/pandas-dev/pandas/pull/60993
        # Surrogates fallback to python storage.
        dtype = pd.StringDtype(storage="python", na_value=np.nan)
    else:
        dtype = "object"
    expected = Series(data, index=Index(data, dtype=dtype), dtype=dtype)
    tm.assert_series_equal(result, expected)

