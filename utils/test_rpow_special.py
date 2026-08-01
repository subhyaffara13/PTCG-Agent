
def test_rpow_special(value, asarray):
    if asarray:
        value = np.array([value])
    result = value**NA

    if asarray:
        result = result[0]
    elif not isinstance(value, (np.float64, np.bool_, np.int_)):
        # this assertion isn't possible with asarray=True
        assert isinstance(result, type(value))

    assert result == value

