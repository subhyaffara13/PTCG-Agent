
def test_fails_on_non_numeric(kernel):
    # GH#46852
    df = DataFrame({"a": [1, 2, 3], "b": object})
    args = (df,) if kernel == "corrwith" else ()
    msg = "|".join(
        [
            "not allowed for this dtype",
            "argument must be a string or a number",
            "not supported between instances of",
            "unsupported operand type",
            "argument must be a string or a real number",
        ]
    )
    if kernel == "median":
        # slightly different message on different builds
        msg1 = (
            r"Cannot convert \[\[<class 'object'> <class 'object'> "
            r"<class 'object'>\]\] to numeric"
        )
        msg2 = (
            r"Cannot convert \[<class 'object'> <class 'object'> "
            r"<class 'object'>\] to numeric"
        )
        msg = "|".join([msg1, msg2])
    with pytest.raises(TypeError, match=msg):
        getattr(df, kernel)(*args)

