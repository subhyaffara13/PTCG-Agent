
def test_three_positional_argument_with_warning_message_analysis():
    msg = (
        f"Starting with pandas version {WARNING_CATEGORY.version()} all arguments of g "
        "except for the argument 'a' will be keyword-only."
    )
    with tm.assert_produces_warning(WARNING_CATEGORY, match=msg):
        assert g(6, 3, 3) == 12

