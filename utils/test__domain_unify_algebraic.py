
def test_Domain_unify_algebraic():
    sqrt5 = QQ.algebraic_field(sqrt(5))
    sqrt7 = QQ.algebraic_field(sqrt(7))
    sqrt57 = QQ.algebraic_field(sqrt(5), sqrt(7))

    assert sqrt5.unify(sqrt7) == sqrt57

    assert sqrt5.unify(sqrt5[x, y]) == sqrt5[x, y]
    assert sqrt5[x, y].unify(sqrt5) == sqrt5[x, y]

    assert sqrt5.unify(sqrt5.frac_field(x, y)) == sqrt5.frac_field(x, y)
    assert sqrt5.frac_field(x, y).unify(sqrt5) == sqrt5.frac_field(x, y)

    assert sqrt5.unify(sqrt7[x, y]) == sqrt57[x, y]
    assert sqrt5[x, y].unify(sqrt7) == sqrt57[x, y]

    assert sqrt5.unify(sqrt7.frac_field(x, y)) == sqrt57.frac_field(x, y)
    assert sqrt5.frac_field(x, y).unify(sqrt7) == sqrt57.frac_field(x, y)

