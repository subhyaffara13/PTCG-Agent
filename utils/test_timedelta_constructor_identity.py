
def test_timedelta_constructor_identity():
    # Test for #30543
    expected = Timedelta(np.timedelta64(1, "s"))
    result = Timedelta(expected)
    assert result is expected

