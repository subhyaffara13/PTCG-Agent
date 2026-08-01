
def test_translated_pattern_match(pattern_match):
    pattern, target = pattern_match
    assert translate_pattern(pattern).match(target)

