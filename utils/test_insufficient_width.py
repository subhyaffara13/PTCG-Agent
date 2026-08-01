
def test_insufficient_width():
    """
    If a 'width' parameter is passed into ``binary_repr`` that is insufficient
    to represent the number in base 2 (positive) or 2's complement (negative)
    form, the function used to silently ignore the parameter and return a
    representation using the minimal number of bits needed for the form in
    question. Such behavior is now considered unsafe from a user perspective
    and will raise an error.
    """
    with pytest.raises(ValueError):
        np.binary_repr(10, width=2)
    with pytest.raises(ValueError):
        np.binary_repr(-5, width=2)

