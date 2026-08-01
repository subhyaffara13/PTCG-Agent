
def test_multiply_dateoffset_typeerror(left, right):
    with pytest.raises(TypeError, match="Cannot multiply"):
        left * right

