
def test_replace_named_groups_regex_swap_expected_fail(
    any_string_dtype, repl, use_compile, request
):
    # GH#57636
    if (
        not use_compile
        and r"\g" not in repl
        and isinstance(any_string_dtype, StringDtype)
        and any_string_dtype.storage == "pyarrow"
    ):
        # calls pyarrow method directly
        if repl == r"\20":
            mark = pytest.mark.xfail(reason="PyArrow interprets as group + literal")
            request.applymarker(mark)

        pa = pytest.importorskip("pyarrow")
        error_type = pa.ArrowInvalid
        error_msg = r"only has \d parenthesized subexpressions"
    else:
        error_type = re.error
        error_msg = "invalid group reference"

    pattern = r"(?P<one>\w+) (?P<two>\w+) (?P<three>\w+)"
    if use_compile:
        pattern = re.compile(pattern)
    ser = Series(["One Two Three", "Foo Bar Baz"], dtype=any_string_dtype)

    with pytest.raises(error_type, match=error_msg):
        ser.str.replace(pattern, repl, regex=True)

