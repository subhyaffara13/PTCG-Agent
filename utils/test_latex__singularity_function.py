
def test_latex_SingularityFunction():
    assert latex(SingularityFunction(x, 4, 5)) == \
        r"{\left\langle x - 4 \right\rangle}^{5}"
    assert latex(SingularityFunction(x, -3, 4)) == \
        r"{\left\langle x + 3 \right\rangle}^{4}"
    assert latex(SingularityFunction(x, 0, 4)) == \
        r"{\left\langle x \right\rangle}^{4}"
    assert latex(SingularityFunction(x, a, n)) == \
        r"{\left\langle - a + x \right\rangle}^{n}"
    assert latex(SingularityFunction(x, 4, -2)) == \
        r"{\left\langle x - 4 \right\rangle}^{-2}"
    assert latex(SingularityFunction(x, 4, -1)) == \
        r"{\left\langle x - 4 \right\rangle}^{-1}"

    assert latex(SingularityFunction(x, 4, 5)**3) == \
        r"{\left({\langle x - 4 \rangle}^{5}\right)}^{3}"
    assert latex(SingularityFunction(x, -3, 4)**3) == \
        r"{\left({\langle x + 3 \rangle}^{4}\right)}^{3}"
    assert latex(SingularityFunction(x, 0, 4)**3) == \
        r"{\left({\langle x \rangle}^{4}\right)}^{3}"
    assert latex(SingularityFunction(x, a, n)**3) == \
        r"{\left({\langle - a + x \rangle}^{n}\right)}^{3}"
    assert latex(SingularityFunction(x, 4, -2)**3) == \
        r"{\left({\langle x - 4 \rangle}^{-2}\right)}^{3}"
    assert latex((SingularityFunction(x, 4, -1)**3)**3) == \
        r"{\left({\langle x - 4 \rangle}^{-1}\right)}^{9}"

