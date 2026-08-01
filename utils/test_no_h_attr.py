
def test_no_H_attr(A):
    with pytest.raises(AttributeError):
        A.H

