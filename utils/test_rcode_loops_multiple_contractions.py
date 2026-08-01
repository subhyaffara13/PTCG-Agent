
def test_rcode_loops_multiple_contractions():
    n, m, o, p = symbols('n m o p', integer=True)
    a = IndexedBase('a')
    b = IndexedBase('b')
    y = IndexedBase('y')
    i = Idx('i', m)
    j = Idx('j', n)
    k = Idx('k', o)
    l = Idx('l', p)

    s = (
        'for (i in 1:m){\n'
        '   y[i] = 0;\n'
        '}\n'
        'for (i in 1:m){\n'
        '   for (j in 1:n){\n'
        '      for (k in 1:o){\n'
        '         for (l in 1:p){\n'
        '            y[i] = a[i, j, k, l]*b[j, k, l] + y[i];\n'
        '         }\n'
        '      }\n'
        '   }\n'
        '}'
    )
    c = rcode(b[j, k, l]*a[i, j, k, l], assign_to=y[i])
    assert c == s

