
def test_Indexed():
    # Issue #10934
    if not numpy:
        skip("numpy not installed")

    a = IndexedBase('a')
    i, j = symbols('i j')
    b = numpy.array([[1, 2], [3, 4]])
    assert lambdify(a, Sum(a[x, y], (x, 0, 1), (y, 0, 1)))(b) == 10


def test_Indexed():
    n, m, o = symbols('n m o', integer=True)
    i, j, k = Idx('i', n), Idx('j', m), Idx('k', o)

    x = IndexedBase('x')[j]
    assert rust_code(x) == "x[j]"

    A = IndexedBase('A')[i, j]
    assert rust_code(A) == "A[m*i + j]"

    B = IndexedBase('B')[i, j, k]
    assert rust_code(B) == "B[m*o*i + o*j + k]"

