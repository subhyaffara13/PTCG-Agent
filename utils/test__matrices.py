
def test_Matrices():
    assert julia_code(Matrix(1, 1, [10])) == "[10]"
    A = Matrix([[1, sin(x/2), abs(x)],
                [0, 1, pi],
                [0, exp(1), ceiling(x)]])
    expected = ("[1 sin(x / 2)  abs(x);\n"
                "0          1      pi;\n"
                "0          e ceil(x)]")
    assert julia_code(A) == expected
    # row and columns
    assert julia_code(A[:,0]) == "[1, 0, 0]"
    assert julia_code(A[0,:]) == "[1 sin(x / 2) abs(x)]"
    # empty matrices
    assert julia_code(Matrix(0, 0, [])) == 'zeros(0, 0)'
    assert julia_code(Matrix(0, 3, [])) == 'zeros(0, 3)'
    # annoying to read but correct
    assert julia_code(Matrix([[x, x - y, -y]])) == "[x x - y -y]"


def test_Matrices():
    assert maple_code(Matrix(1, 1, [10])) == \
           'Matrix([[10]], storage = rectangular)'

    A = Matrix([[1, sin(x / 2), abs(x)],
                [0, 1, pi],
                [0, exp(1), ceiling(x)]])
    expected = \
        'Matrix(' \
        '[[1, sin((1/2)*x), abs(x)],' \
        ' [0, 1, Pi],' \
        ' [0, exp(1), ceil(x)]], ' \
        'storage = rectangular)'
    assert maple_code(A) == expected

    # row and columns
    assert maple_code(A[:, 0]) == \
           'Matrix([[1], [0], [0]], storage = rectangular)'
    assert maple_code(A[0, :]) == \
           'Matrix([[1, sin((1/2)*x), abs(x)]], storage = rectangular)'
    assert maple_code(Matrix([[x, x - y, -y]])) == \
           'Matrix([[x, x - y, -y]], storage = rectangular)'

    # empty matrices
    assert maple_code(Matrix(0, 0, [])) == \
           'Matrix([], storage = rectangular)'
    assert maple_code(Matrix(0, 3, [])) == \
           'Matrix([], storage = rectangular)'


def test_Matrices():
    assert mcode(Matrix(1, 1, [10])) == "10"
    A = Matrix([[1, sin(x/2), abs(x)],
                [0, 1, pi],
                [0, exp(1), ceiling(x)]])
    expected = "[1 sin(x/2) abs(x); 0 1 pi; 0 exp(1) ceil(x)]"
    assert mcode(A) == expected
    # row and columns
    assert mcode(A[:,0]) == "[1; 0; 0]"
    assert mcode(A[0,:]) == "[1 sin(x/2) abs(x)]"
    # empty matrices
    assert mcode(Matrix(0, 0, [])) == '[]'
    assert mcode(Matrix(0, 3, [])) == 'zeros(0, 3)'
    # annoying to read but correct
    assert mcode(Matrix([[x, x - y, -y]])) == "[x x - y -y]"

