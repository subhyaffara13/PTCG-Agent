
def test_ccode_loops_add():
    n, m = symbols('n m', integer=True)
    A = IndexedBase('A')
    x = IndexedBase('x')
    y = IndexedBase('y')
    z = IndexedBase('z')
    i = Idx('i', m)
    j = Idx('j', n)

    s = (
        'for (int i=0; i<m; i++){\n'
        '   y[i] = x[i] + z[i];\n'
        '}\n'
        'for (int i=0; i<m; i++){\n'
        '   for (int j=0; j<n; j++){\n'
        '      y[i] = A[%s]*x[j] + y[i];\n' % (i*n + j) +\
        '   }\n'
        '}'
    )
    assert ccode(A[i, j]*x[j] + x[i] + z[i], assign_to=y[i]) == s

