
def test_lfilter_notimplemented_input(xp):
    # Should not crash, gh-7991
    assert_raises(NotImplementedError, lfilter, [2,3], [4,5], [1,2,3,4,5])

