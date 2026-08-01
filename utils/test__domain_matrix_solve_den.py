
def test_DomainMatrix_solve_den():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    result = DomainMatrix([[ZZ(0)], [ZZ(-1)]], (2, 1), ZZ)
    den = ZZ(-2)
    _check_solve_den(A, b, result, den)

    A = DomainMatrix([
        [ZZ(1), ZZ(2), ZZ(3)],
        [ZZ(1), ZZ(2), ZZ(4)],
        [ZZ(1), ZZ(3), ZZ(5)]], (3, 3), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(2)], [ZZ(3)]], (3, 1), ZZ)
    result = DomainMatrix([[ZZ(2)], [ZZ(0)], [ZZ(-1)]], (3, 1), ZZ)
    den = ZZ(-1)
    _check_solve_den(A, b, result, den)

    A = DomainMatrix([[ZZ(2)], [ZZ(2)]], (2, 1), ZZ)
    b = DomainMatrix([[ZZ(3)], [ZZ(3)]], (2, 1), ZZ)
    result = DomainMatrix([[ZZ(3)]], (1, 1), ZZ)
    den = ZZ(2)
    _check_solve_den(A, b, result, den)

