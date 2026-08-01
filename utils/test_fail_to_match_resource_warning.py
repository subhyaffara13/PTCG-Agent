
def test_fail_to_match_resource_warning():
    category = ResourceWarning
    match = r"\d+"
    unmatched = (
        r"Did not see warning 'ResourceWarning' matching '\\d\+'. "
        r"The emitted warning messages are "
        r"\[ResourceWarning\('This is not a match.'\), "
        r"ResourceWarning\('Another unmatched warning.'\)\]"
    )
    with pytest.raises(AssertionError, match=unmatched):
        with tm.assert_produces_warning(category, match=match):
            warnings.warn("This is not a match.", category)
            warnings.warn("Another unmatched warning.", category)

