
def test_rcode_Indexed():
    n, m, o = symbols('n m o', integer=True)
    i, j, k = Idx('i', n), Idx('j', m), Idx('k', o)
    p = RCodePrinter()
    p._not_r = set()

    x = IndexedBase('x')[j]
    assert p._print_Indexed(x) == 'x[j]'
    A = IndexedBase('A')[i, j]
    assert p._print_Indexed(A) == 'A[i, j]'
    B = IndexedBase('B')[i, j, k]
    assert p._print_Indexed(B) == 'B[i, j, k]'

    assert p._not_r == set()

