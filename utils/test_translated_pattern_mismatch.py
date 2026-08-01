
def test_translated_pattern_mismatch(pattern_mismatch):
    pattern, target = pattern_mismatch
    assert not translate_pattern(pattern).match(target)

