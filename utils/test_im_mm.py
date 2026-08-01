
def test_IM_MM():
    assert isinstance(MM + IM, ImmutableMatrix)
    assert isinstance(IM + MM, ImmutableMatrix)
    assert isinstance(2*IM + MM, ImmutableMatrix)
    assert MM.equals(IM)

