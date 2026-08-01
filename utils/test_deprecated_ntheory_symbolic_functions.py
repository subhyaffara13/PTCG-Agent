
def test_deprecated_ntheory_symbolic_functions():
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        assert primenu(3) == 1
    with warns_deprecated_sympy():
        assert primeomega(3) == 1
    with warns_deprecated_sympy():
        assert totient(3) == 2
    with warns_deprecated_sympy():
        assert reduced_totient(3) == 2
    with warns_deprecated_sympy():
        assert divisor_sigma(3) == 4
    with warns_deprecated_sympy():
        assert udivisor_sigma(3) == 4


def test_deprecated_ntheory_symbolic_functions():
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        assert primepi(0) == 0


def test_deprecated_ntheory_symbolic_functions():
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        assert npartitions(0) == 1


def test_deprecated_ntheory_symbolic_functions():
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        assert mobius(3) == -1
    with warns_deprecated_sympy():
        assert legendre_symbol(2, 3) == -1
    with warns_deprecated_sympy():
        assert jacobi_symbol(2, 3) == -1


def test_deprecated_ntheory_symbolic_functions():
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        assert not carmichael.is_carmichael(3)
    with warns_deprecated_sympy():
        assert carmichael.find_carmichael_numbers_in_range(10, 20) == []
    with warns_deprecated_sympy():
        assert carmichael.find_first_n_carmichaels(1)

