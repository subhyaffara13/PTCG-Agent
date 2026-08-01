
def test_error_both_scalar(operation):
    msg = r"Either `left` or `right` need to be an np\.ndarray."
    with pytest.raises(TypeError, match=msg):
        # masks need to be non-None, otherwise it ends up in an infinite recursion
        operation(True, True, np.zeros(1), np.zeros(1))

