
def test_X20():
    # Pade (rational function) approximation => (2 - x)/(2 + x)
    # > numapprox[pade](exp(-x), x = 0, [1, 1]);
    # bytes used=9019816, alloc=3669344, time=13.12
    #                                    1 - 1/2 x
    #                                    ---------
    #                                    1 + 1/2 x
    # mpmath support numeric Pade approximant but there is
    # no symbolic implementation in SymPy
    # https://en.wikipedia.org/wiki/Pad%C3%A9_approximant
    raise NotImplementedError("Symbolic Pade approximant not supported")

