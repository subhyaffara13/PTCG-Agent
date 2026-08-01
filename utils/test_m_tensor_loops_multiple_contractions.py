
def test_m_tensor_loops_multiple_contractions():
    # see comments in previous test about vectorizing
    from sympy.tensor import IndexedBase, Idx
    from sympy.core.symbol import symbols
    n, m, o, p = symbols('n m o p', integer=True)
    A = IndexedBase('A')
    B = IndexedBase('B')
    y = IndexedBase('y')
    i = Idx('i', m)
    j = Idx('j', n)
    k = Idx('k', o)
    l = Idx('l', p)
    result, = codegen(('tensorthing', Eq(y[i], B[j, k, l]*A[i, j, k, l])),
                      "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        'function y = tensorthing(A, B, m, n, o, p)\n'
        '  for i = 1:m\n'
        '    y(i) = 0;\n'
        '  end\n'
        '  for i = 1:m\n'
        '    for j = 1:n\n'
        '      for k = 1:o\n'
        '        for l = 1:p\n'
        '          y(i) = A(i, j, k, l).*B(j, k, l) + y(i);\n'
        '        end\n'
        '      end\n'
        '    end\n'
        '  end\n'
        'end\n'
    )
    assert source == expected

