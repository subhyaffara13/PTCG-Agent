
def test_LUdecomposition_Simple_iszerofunc():
    # Test if callable passed to matrices.LUdecomposition_Simple() as iszerofunc keyword argument is used inside
    # matrices.LUdecomposition_Simple()
    magic_string = "I got passed in!"
    def goofyiszero(value):
        raise ValueError(magic_string)

    try:
        lu, p = Matrix([[1, 0], [0, 1]]).LUdecomposition_Simple(iszerofunc=goofyiszero)
    except ValueError as err:
        assert magic_string == err.args[0]
        return

    assert False

