
def test_ModularInteger():
    F3 = FF(3)

    a = F3(0)
    assert F3.of_type(a) and a == 0
    a = F3(1)
    assert F3.of_type(a) and a == 1
    a = F3(2)
    assert F3.of_type(a) and a == 2
    a = F3(3)
    assert F3.of_type(a) and a == 0
    a = F3(4)
    assert F3.of_type(a) and a == 1

    a = F3(F3(0))
    assert F3.of_type(a) and a == 0
    a = F3(F3(1))
    assert F3.of_type(a) and a == 1
    a = F3(F3(2))
    assert F3.of_type(a) and a == 2
    a = F3(F3(3))
    assert F3.of_type(a) and a == 0
    a = F3(F3(4))
    assert F3.of_type(a) and a == 1

    a = -F3(1)
    assert F3.of_type(a) and a == 2
    a = -F3(2)
    assert F3.of_type(a) and a == 1

    a = 2 + F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(2) + 2
    assert F3.of_type(a) and a == 1
    a = F3(2) + F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(2) + F3(2)
    assert F3.of_type(a) and a == 1

    a = 3 - F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(3) - 2
    assert F3.of_type(a) and a == 1
    a = F3(3) - F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(3) - F3(2)
    assert F3.of_type(a) and a == 1

    a = 2*F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(2)*2
    assert F3.of_type(a) and a == 1
    a = F3(2)*F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(2)*F3(2)
    assert F3.of_type(a) and a == 1

    a = 2/F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(2)/2
    assert F3.of_type(a) and a == 1
    a = F3(2)/F3(2)
    assert F3.of_type(a) and a == 1
    a = F3(2)/F3(2)
    assert F3.of_type(a) and a == 1

    a = F3(2)**0
    assert F3.of_type(a) and a == 1
    a = F3(2)**1
    assert F3.of_type(a) and a == 2
    a = F3(2)**2
    assert F3.of_type(a) and a == 1

    F7 = FF(7)

    a = F7(3)**100000000000
    assert F7.of_type(a) and a == 4
    a = F7(3)**-100000000000
    assert F7.of_type(a) and a == 2

    assert bool(F3(3)) is False
    assert bool(F3(4)) is True

    F5 = FF(5)

    a = F5(1)**(-1)
    assert F5.of_type(a) and a == 1
    a = F5(2)**(-1)
    assert F5.of_type(a) and a == 3
    a = F5(3)**(-1)
    assert F5.of_type(a) and a == 2
    a = F5(4)**(-1)
    assert F5.of_type(a) and a == 4

    if GROUND_TYPES != 'flint':
        # XXX: This gives a core dump with python-flint...
        raises(NotInvertible, lambda: F5(0)**(-1))
        raises(NotInvertible, lambda: F5(5)**(-1))

    raises(ValueError, lambda: FF(0))
    raises(ValueError, lambda: FF(2.1))

    for n1 in range(5):
        for n2 in range(5):
            if GROUND_TYPES != 'flint':
                with warns_deprecated_sympy():
                    assert (F5(n1) < F5(n2)) is (n1 < n2)
                with warns_deprecated_sympy():
                    assert (F5(n1) <= F5(n2)) is (n1 <= n2)
                with warns_deprecated_sympy():
                    assert (F5(n1) > F5(n2)) is (n1 > n2)
                with warns_deprecated_sympy():
                    assert (F5(n1) >= F5(n2)) is (n1 >= n2)
            else:
                raises(TypeError, lambda: F5(n1) < F5(n2))
                raises(TypeError, lambda: F5(n1) <= F5(n2))
                raises(TypeError, lambda: F5(n1) > F5(n2))
                raises(TypeError, lambda: F5(n1) >= F5(n2))

    # https://github.com/sympy/sympy/issues/26789
    assert GF(Integer(5)) == F5
    assert F5(Integer(3)) == F5(3)

