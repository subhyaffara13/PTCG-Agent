
def test_rcode_loops_matrix_vector():
    n, m = symbols('n m', integer=True)
    A = IndexedBase('A')
    x = IndexedBase('x')
    y = IndexedBase('y')
    i = Idx('i', m)
    j = Idx('j', n)

    s = (
        'for (i in 1:m){\n'
        '   y[i] = 0;\n'
        '}\n'
        'for (i in 1:m){\n'
        '   for (j in 1:n){\n'
        '      y[i] = A[i, j]*x[j] + y[i];\n'
        '   }\n'
        '}'
    )
    c = rcode(A[i, j]*x[j], assign_to=y[i])
    assert c == s

