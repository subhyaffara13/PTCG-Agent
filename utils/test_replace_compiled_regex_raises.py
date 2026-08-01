
def test_replace_compiled_regex_raises(any_string_dtype):
    # case and flags provided to str.replace will have no effect
    # and will produce warnings
    ser = Series(["fooBAD__barBAD__bad", np.nan], dtype=any_string_dtype)
    pat = re.compile(r"BAD_*")

    msg = "case and flags cannot be set when pat is a compiled regex"

    with pytest.raises(ValueError, match=msg):
        ser.str.replace(pat, "", flags=re.IGNORECASE, regex=True)

    with pytest.raises(ValueError, match=msg):
        ser.str.replace(pat, "", case=False, regex=True)

    with pytest.raises(ValueError, match=msg):
        ser.str.replace(pat, "", case=True, regex=True)

