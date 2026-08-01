
def test_deprecated_print_cyclic():
    p = Permutation(0, 1, 2)
    try:
        Permutation.print_cyclic = True
        with warns_deprecated_sympy():
            assert sstr(p) == '(0 1 2)'
        with warns_deprecated_sympy():
            assert srepr(p) == 'Permutation(0, 1, 2)'
        with warns_deprecated_sympy():
            assert pretty(p) == '(0 1 2)'
        with warns_deprecated_sympy():
            assert latex(p) == r'\left( 0\; 1\; 2\right)'

        Permutation.print_cyclic = False
        with warns_deprecated_sympy():
            assert sstr(p) == 'Permutation([1, 2, 0])'
        with warns_deprecated_sympy():
            assert srepr(p) == 'Permutation([1, 2, 0])'
        with warns_deprecated_sympy():
            assert pretty(p, use_unicode=False) == '/0 1 2\\\n\\1 2 0/'
        with warns_deprecated_sympy():
            assert latex(p) == \
                r'\begin{pmatrix} 0 & 1 & 2 \\ 1 & 2 & 0 \end{pmatrix}'
    finally:
        Permutation.print_cyclic = None

