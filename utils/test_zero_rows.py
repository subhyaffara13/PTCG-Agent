
def test_zero_rows(datapath, encoding):
    # GH 18198
    fname = datapath("io", "sas", "data", "zero_rows.sas7bdat")
    result = pd.read_sas(fname, encoding=encoding)
    str_value = b"a" if encoding is None else "a"
    expected = pd.DataFrame([{"char_field": str_value, "num_field": 1.0}]).iloc[:0]
    tm.assert_frame_equal(result, expected)

