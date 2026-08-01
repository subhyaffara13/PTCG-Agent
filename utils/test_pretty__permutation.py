
def test_pretty_Permutation():
    from sympy.combinatorics.permutations import Permutation
    p1 = Permutation(1, 2)(3, 4)
    assert xpretty(p1, perm_cyclic=True, use_unicode=True) == "(1 2)(3 4)"
    assert xpretty(p1, perm_cyclic=True, use_unicode=False) == "(1 2)(3 4)"
    assert xpretty(p1, perm_cyclic=False, use_unicode=True) == \
    '⎛0 1 2 3 4⎞\n'\
    '⎝0 2 1 4 3⎠'
    assert xpretty(p1, perm_cyclic=False, use_unicode=False) == \
    "/0 1 2 3 4\\\n"\
    "\\0 2 1 4 3/"

    with warns_deprecated_sympy():
        old_print_cyclic = Permutation.print_cyclic
        Permutation.print_cyclic = False
        assert xpretty(p1, use_unicode=True) == \
        '⎛0 1 2 3 4⎞\n'\
        '⎝0 2 1 4 3⎠'
        assert xpretty(p1, use_unicode=False) == \
        "/0 1 2 3 4\\\n"\
        "\\0 2 1 4 3/"
        Permutation.print_cyclic = old_print_cyclic

