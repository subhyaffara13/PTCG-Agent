
def test_logical_or():
    assert NA | True is True
    assert True | NA is True
    assert NA | False is NA
    assert False | NA is NA
    assert NA | NA is NA

    # GH#58427
    assert NA | np.bool_(True) is True
    assert np.bool_(True) | NA is True
    assert NA | np.bool_(False) is NA
    assert np.bool_(False) | NA is NA

    msg = "unsupported operand type"
    with pytest.raises(TypeError, match=msg):
        NA | 5

