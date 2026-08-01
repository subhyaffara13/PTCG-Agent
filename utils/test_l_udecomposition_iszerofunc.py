
def test_LUdecomposition_iszerofunc():
    # Test if callable passed to matrices.LUdecomposition() as iszerofunc keyword argument is used inside
    # matrices.LUdecomposition_Simple()
    magic_string = "I got passed in!"
    def goofyiszero(value):
        raise ValueError(magic_string)

    try:
        l, u, p = Matrix([[1, 0], [0, 1]]).LUdecomposition(iszerofunc=goofyiszero)
    except ValueError as err:
        assert magic_string == err.args[0]
        return

    assert False

