
def test_replace_callable_raises(any_string_dtype, repl):
    # GH 15055
    values = Series(["fooBAD__barBAD", np.nan], dtype=any_string_dtype)

    # test with wrong number of arguments, raising an error
    msg = (
        r"((takes)|(missing)) (?(2)from \d+ to )?\d+ "
        r"(?(3)required )positional arguments?"
    )
    with pytest.raises(TypeError, match=msg):
        values.str.replace("a", repl, regex=True)

