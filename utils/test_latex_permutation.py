
def test_latex_permutation():
    assert latex(Permutation(1, 2, 4)) == r"\left( 1\; 2\; 4\right)"
    assert latex(Permutation(1, 2)(4, 5, 6)) == \
        r"\left( 1\; 2\right)\left( 4\; 5\; 6\right)"
    assert latex(Permutation()) == r"\left( \right)"
    assert latex(Permutation(2, 4)*Permutation(5)) == \
        r"\left( 2\; 4\right)\left( 5\right)"
    assert latex(Permutation(5)) == r"\left( 5\right)"

    assert latex(Permutation(0, 1), perm_cyclic=False) == \
        r"\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}"
    assert latex(Permutation(0, 1)(2, 3), perm_cyclic=False) == \
        r"\begin{pmatrix} 0 & 1 & 2 & 3 \\ 1 & 0 & 3 & 2 \end{pmatrix}"
    assert latex(Permutation(), perm_cyclic=False) == \
        r"\left( \right)"

    with warns_deprecated_sympy():
        old_print_cyclic = Permutation.print_cyclic
        Permutation.print_cyclic = False
        assert latex(Permutation(0, 1)(2, 3)) == \
            r"\begin{pmatrix} 0 & 1 & 2 & 3 \\ 1 & 0 & 3 & 2 \end{pmatrix}"
        Permutation.print_cyclic = old_print_cyclic

