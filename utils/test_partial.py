
def test_partial():
    assert copy(Machine(), byref=True)
    assert copy(Machine(), byref=True, recurse=True)
    assert copy(Machine(), recurse=True)
    assert copy(Machine())

