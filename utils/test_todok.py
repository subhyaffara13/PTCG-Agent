
def test_todok():
    a, b, c, d = symbols('a:d')
    m1 = MutableDenseMatrix([[a, b], [c, d]])
    m2 = ImmutableDenseMatrix([[a, b], [c, d]])
    m3 = MutableSparseMatrix([[a, b], [c, d]])
    m4 = ImmutableSparseMatrix([[a, b], [c, d]])
    assert m1.todok() == m2.todok() == m3.todok() == m4.todok() == \
        {(0, 0): a, (0, 1): b, (1, 0): c, (1, 1): d}


def test_todok():
    a, b, c, d = symbols('a:d')
    m1 = MutableDenseMatrix([[a, b], [c, d]])
    m2 = ImmutableDenseMatrix([[a, b], [c, d]])
    m3 = MutableSparseMatrix([[a, b], [c, d]])
    m4 = ImmutableSparseMatrix([[a, b], [c, d]])
    assert m1.todok() == m2.todok() == m3.todok() == m4.todok() == \
        {(0, 0): a, (0, 1): b, (1, 0): c, (1, 1): d}

