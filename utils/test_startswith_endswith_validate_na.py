
def test_startswith_endswith_validate_na(any_string_dtype):
    # GH#59615
    ser = Series(
        ["om", np.nan, "foo_nom", "nom", "bar_foo", np.nan, "foo"],
        dtype=any_string_dtype,
    )
    msg = "na must be None, pd.NA, np.nan, True, or False; got baz"
    with pytest.raises(ValueError, match=msg):
        ser.str.startswith("kapow", na="baz")
    with pytest.raises(ValueError, match=msg):
        ser.str.endswith("bar", na="baz")

