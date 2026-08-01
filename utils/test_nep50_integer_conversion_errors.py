
def test_nep50_integer_conversion_errors():
    # Implementation for error paths is mostly missing (as of writing)
    with pytest.raises(OverflowError, match=".*uint8"):
        np.array([1], np.uint8) + 300

    with pytest.raises(OverflowError, match=".*uint8"):
        np.uint8(1) + 300

    # Error message depends on platform (maybe unsigned int or unsigned long)
    with pytest.raises(OverflowError,
            match="Python integer -1 out of bounds for uint8"):
        np.uint8(1) + -1

