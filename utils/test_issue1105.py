
def test_issue1105():
    """Issue 1105: 1xN or Nx1 input arrays weren't accepted for eigen
    compile-time row vectors or column vector"""
    assert m.iss1105_row(np.ones((1, 7)))
    assert m.iss1105_col(np.ones((7, 1)))

    # These should still fail (incompatible dimensions):
    with pytest.raises(TypeError) as excinfo:
        m.iss1105_row(np.ones((7, 1)))
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.iss1105_col(np.ones((1, 7)))
    assert "incompatible function arguments" in str(excinfo.value)

