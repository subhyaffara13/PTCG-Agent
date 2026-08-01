
def test_singleton():
    assert NA is NA
    new_NA = type(NA)()
    assert new_NA is NA

