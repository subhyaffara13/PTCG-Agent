
def test_same_category_different_messages_last_match():
    category = DeprecationWarning
    with tm.assert_produces_warning(category, match=r"^Match this"):
        warnings.warn("Do not match that", category)
        warnings.warn("Do not match that either", category)
        warnings.warn("Match this", category)

