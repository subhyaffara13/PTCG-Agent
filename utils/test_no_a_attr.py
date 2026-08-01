
def test_no_A_attr(A):
    with pytest.raises(AttributeError):
        A.A

