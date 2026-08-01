
def test_logical_and():
    assert NA & True is NA
    assert True & NA is NA
    assert NA & False is False
    assert False & NA is False
    assert NA & NA is NA

    # GH#58427
    assert NA & np.bool_(True) is NA
    assert np.bool_(True) & NA is NA
    assert NA & np.bool_(False) is False
    assert np.bool_(False) & NA is False

    msg = "unsupported operand type"
    with pytest.raises(TypeError, match=msg):
        NA & 5

