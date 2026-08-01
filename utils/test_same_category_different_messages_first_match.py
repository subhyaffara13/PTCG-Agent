
def test_same_category_different_messages_first_match():
    category = UserWarning
    with tm.assert_produces_warning(category, match=r"^Match this"):
        warnings.warn("Match this", category)
        warnings.warn("Do not match that", category)
        warnings.warn("Do not match that either", category)

