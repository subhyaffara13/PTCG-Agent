
def test_arbitrary_number_of_ops_error():
    # A different error may happen for more than integer operands, but that
    # is too large to test nicely.
    a = np.ones(1)
    args = [a] * (np.iinfo(np.intc).max + 1)
    with pytest.raises(ValueError, match="Too many operands to nditer"):
        np.nditer(args)

    with pytest.raises(ValueError, match="Too many operands to nditer"):
        np.nested_iters(args, [[0], []])

