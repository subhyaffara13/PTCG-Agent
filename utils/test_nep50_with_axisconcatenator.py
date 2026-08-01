
def test_nep50_with_axisconcatenator():
    # Concatenate/r_ does not promote, so this has to error:
    with pytest.raises(OverflowError):
        np.r_[np.arange(5, dtype=np.int8), 255]

