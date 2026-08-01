
def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert(ccode(A[0, 0]) == "A[0]")
    assert(ccode(3 * A[0, 0]) == "3*A[0]")

    F = C[0, 0].subs(C, A - B)
    assert(ccode(F) == "(A - B)[0]")


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert(fcode(A[0, 0]) == "      A(1, 1)")
    assert(fcode(3 * A[0, 0]) == "      3*A(1, 1)")

    F = C[0, 0].subs(C, A - B)
    assert(fcode(F) == "      (A - B)(1, 1)")


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert(jscode(A[0, 0]) == "A[0]")
    assert(jscode(3 * A[0, 0]) == "3*A[0]")

    F = C[0, 0].subs(C, A - B)
    assert(jscode(F) == "(A - B)[0]")


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert(julia_code(A[0, 0]) == "A[1,1]")
    assert(julia_code(3 * A[0, 0]) == "3 * A[1,1]")

    F = C[0, 0].subs(C, A - B)
    assert(julia_code(F) == "(A - B)[1,1]")


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert latex(A[0, 0]) == r"{A}_{0,0}"
    assert latex(3 * A[0, 0]) == r"3 {A}_{0,0}"

    F = C[0, 0].subs(C, A - B)
    assert latex(F) == r"{\left(A - B\right)}_{0,0}"

    i, j, k = symbols("i j k")
    M = MatrixSymbol("M", k, k)
    N = MatrixSymbol("N", k, k)
    assert latex((M*N)[i, j]) == \
        r'\sum_{i_{1}=0}^{k - 1} {M}_{i,i_{1}} {N}_{i_{1},j}'

    X_a = MatrixSymbol('X_a', 3, 3)
    assert latex(X_a[0, 0]) == r"{X_{a}}_{0,0}"


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)

    assert (maple_code(A[0, 0]) == "A[1, 1]")
    assert (maple_code(3 * A[0, 0]) == "3*A[1, 1]")

    F = A-B

    assert (maple_code(F[0,0]) == "A[1, 1] - B[1, 1]")


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert mcode(A[0, 0]) == "A(1, 1)"
    assert mcode(3 * A[0, 0]) == "3*A(1, 1)"

    F = C[0, 0].subs(C, A - B)
    assert mcode(F) == "(A - B)(1, 1)"


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert(rcode(A[0, 0]) == "A[0]")
    assert(rcode(3 * A[0, 0]) == "3*A[0]")

    F = C[0, 0].subs(C, A - B)
    assert(rcode(F) == "(A - B)[0]")


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert(str(A[0, 0]) == "A[0, 0]")
    assert(str(3 * A[0, 0]) == "3*A[0, 0]")

    F = C[0, 0].subs(C, A - B)
    assert str(F) == "(A - B)[0, 0]"


def test_MatrixElement_printing():
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    assert tensorflow_code(A[0, 0]) == "A[0, 0]"
    assert tensorflow_code(3 * A[0, 0]) == "3*A[0, 0]"

    F = C[0, 0].subs(C, A - B)
    assert tensorflow_code(F) == "(tensorflow.math.add((-1)*B, A))[0, 0]"


def test_MatrixElement_printing():
    # test cases for issue #11821
    A = MatrixSymbol("A", 1, 3)
    B = MatrixSymbol("B", 1, 3)
    C = MatrixSymbol("C", 1, 3)

    ascii_str1 = "A_00"
    ucode_str1 = "A₀₀"
    assert pretty(A[0, 0])  == ascii_str1
    assert upretty(A[0, 0]) == ucode_str1

    ascii_str1 = "3*A_00"
    ucode_str1 = "3⋅A₀₀"
    assert pretty(3*A[0, 0])  == ascii_str1
    assert upretty(3*A[0, 0]) == ucode_str1

    ascii_str1 = "(-B + A)[0, 0]"
    ucode_str1 = "(-B + A)[0, 0]"
    F = C[0, 0].subs(C, A - B)
    assert pretty(F)  == ascii_str1
    assert upretty(F) == ucode_str1

