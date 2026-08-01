
def test_Matrices_entries_not_hadamard():
    # For Matrix with col >= 2, row >= 2, they need to be scalars
    # FIXME: is it worth worrying about this?  Its not wrong, just
    # leave it user's responsibility to put scalar data for x.
    A = Matrix([[1, sin(2/x), 3*pi/x/5], [1, 2, x*y]])
    expected = ("[1 sin(2/x) 3*pi/(5*x);\n"
                "1        2        x*y]") # <- we give x.*y
    assert julia_code(A) == expected


def test_Matrices_entries_not_hadamard():
    A = Matrix([[1, sin(2 / x), 3 * pi / x / 5], [1, 2, x * y]])
    expected = \
        'Matrix([[1, sin(2/x), (3/5)*Pi/x], [1, 2, x*y]], ' \
        'storage = rectangular)'
    assert maple_code(A) == expected


def test_Matrices_entries_not_hadamard():
    # For Matrix with col >= 2, row >= 2, they need to be scalars
    # FIXME: is it worth worrying about this?  Its not wrong, just
    # leave it user's responsibility to put scalar data for x.
    A = Matrix([[1, sin(2/x), 3*pi/x/5], [1, 2, x*y]])
    expected = ("[1 sin(2/x) 3*pi/(5*x);\n"
                "1        2        x*y]") # <- we give x.*y
    assert mcode(A) == expected

