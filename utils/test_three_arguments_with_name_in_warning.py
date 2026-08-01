
def test_three_arguments_with_name_in_warning():
    msg = (
        f"Starting with pandas version {WARNING_CATEGORY.version()} all arguments of "
        "f_add_inputs except for the arguments 'a' and 'b' will be keyword-only."
    )
    with tm.assert_produces_warning(WARNING_CATEGORY, match=msg):
        assert f(6, 3, 3) == 12

