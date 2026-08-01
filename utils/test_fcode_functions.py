
def test_fcode_functions():
    x, y = symbols('x,y')
    assert fcode(sin(x) ** cos(y)) == "      sin(x)**cos(y)"
    raises(NotImplementedError, lambda: fcode(Mod(x, y), standard=66))
    raises(NotImplementedError, lambda: fcode(x % y, standard=66))
    raises(NotImplementedError, lambda: fcode(Mod(x, y), standard=77))
    raises(NotImplementedError, lambda: fcode(x % y, standard=77))
    for standard in [90, 95, 2003, 2008]:
        assert fcode(Mod(x, y), standard=standard) == "      modulo(x, y)"
        assert fcode(x % y, standard=standard) == "      modulo(x, y)"

