
def test_extract_expand_kwarg_wrong_type_raises(any_string_dtype):
    # TODO: should this raise TypeError
    values = Series(["fooBAD__barBAD", np.nan, "foo"], dtype=any_string_dtype)
    with pytest.raises(ValueError, match="expand must be True or False"):
        values.str.extract(".*(BAD[_]+).*(BAD)", expand=None)

