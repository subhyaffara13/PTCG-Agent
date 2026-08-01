
def test_one_positional_argument_with_warning_message_analysis():
    msg = (
        f"Starting with pandas version {WARNING_CATEGORY.version()} all arguments "
        "of h will be keyword-only."
    )
    with tm.assert_produces_warning(WARNING_CATEGORY, match=msg):
        assert h(19) == 19

