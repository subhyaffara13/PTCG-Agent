
def test_to_array_error(values):
    # error in converting existing arrays to FloatingArray
    msg = "|".join(
        [
            "cannot be converted to FloatingDtype",
            "values must be a 1D list-like",
            "Cannot pass scalar",
            r"float\(\) argument must be a string or a (real )?number, not 'dict'",
            "could not convert string to float: 'foo'",
            r"could not convert string to float: np\.str_\('foo'\)",
        ]
    )
    with pytest.raises((TypeError, ValueError), match=msg):
        pd.array(values, dtype="Float64")

