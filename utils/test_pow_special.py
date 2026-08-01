
def test_pow_special(value, asarray):
    if asarray:
        value = np.array([value])
    result = NA**value

    if asarray:
        result = result[0]
    else:
        # this assertion isn't possible for ndarray.
        assert isinstance(result, type(value))
    assert result == 1

