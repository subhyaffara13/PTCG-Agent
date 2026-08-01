
def test_vector_entries_hadamard():
    # For a row or column, user might to use the other dimension
    A = Matrix([[1, sin(2/x), 3*pi/x/5]])
    assert julia_code(A) == "[1 sin(2 ./ x) (3 // 5) * pi ./ x]"
    assert julia_code(A.T) == "[1, sin(2 ./ x), (3 // 5) * pi ./ x]"


def test_vector_entries_hadamard():
    # For a row or column, user might to use the other dimension
    A = Matrix([[1, sin(2 / x), 3 * pi / x / 5]])
    assert maple_code(A) == \
           'Matrix([[1, sin(2/x), (3/5)*Pi/x]], storage = rectangular)'
    assert maple_code(A.T) == \
           'Matrix([[1], [sin(2/x)], [(3/5)*Pi/x]], storage = rectangular)'


def test_vector_entries_hadamard():
    # For a row or column, user might to use the other dimension
    A = Matrix([[1, sin(2/x), 3*pi/x/5]])
    assert mcode(A) == "[1 sin(2./x) 3*pi./(5*x)]"
    assert mcode(A.T) == "[1; sin(2./x); 3*pi./(5*x)]"

