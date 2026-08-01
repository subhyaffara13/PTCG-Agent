
def test_catch_warning_category_and_match(category, message, match):
    with tm.assert_produces_warning(category, match=match):
        warnings.warn(message, category)

