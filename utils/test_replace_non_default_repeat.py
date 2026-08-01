
def test_replace_non_default_repeat(count):
    a = np.array(["🐍--", "🦜-🦜-"], "T")
    result = np.strings.replace(a, "🦜-", "🦜†", count)
    assert_array_equal(result, np.array(["🐍--", "🦜†🦜†"], "T"))

