
def test_Permutation_Cycle():
    from sympy.combinatorics import Permutation, Cycle

    # general principle: economically, canonically show all moved elements
    # and the size of the permutation.

    for p, s in [
        (Cycle(),
        '()'),
        (Cycle(2),
        '(2)'),
        (Cycle(2, 1),
        '(1 2)'),
        (Cycle(1, 2)(5)(6, 7)(10),
        '(1 2)(6 7)(10)'),
        (Cycle(3, 4)(1, 2)(3, 4),
        '(1 2)(4)'),
    ]:
        assert sstr(p) == s

    for p, s in [
        (Permutation([]),
        'Permutation([])'),
        (Permutation([], size=1),
        'Permutation([0])'),
        (Permutation([], size=2),
        'Permutation([0, 1])'),
        (Permutation([], size=10),
        'Permutation([], size=10)'),
        (Permutation([1, 0, 2]),
        'Permutation([1, 0, 2])'),
        (Permutation([1, 0, 2, 3, 4, 5]),
        'Permutation([1, 0], size=6)'),
        (Permutation([1, 0, 2, 3, 4, 5], size=10),
        'Permutation([1, 0], size=10)'),
    ]:
        assert sstr(p, perm_cyclic=False) == s

    for p, s in [
        (Permutation([]),
        '()'),
        (Permutation([], size=1),
        '(0)'),
        (Permutation([], size=2),
        '(1)'),
        (Permutation([], size=10),
        '(9)'),
        (Permutation([1, 0, 2]),
        '(2)(0 1)'),
        (Permutation([1, 0, 2, 3, 4, 5]),
        '(5)(0 1)'),
        (Permutation([1, 0, 2, 3, 4, 5], size=10),
        '(9)(0 1)'),
        (Permutation([0, 1, 3, 2, 4, 5], size=10),
        '(9)(2 3)'),
    ]:
        assert sstr(p) == s


    with warns_deprecated_sympy():
        old_print_cyclic = Permutation.print_cyclic
        Permutation.print_cyclic = False
        assert sstr(Permutation([1, 0, 2])) == 'Permutation([1, 0, 2])'
        Permutation.print_cyclic = old_print_cyclic

