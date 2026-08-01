
def test_bosonoperator():
    a = BosonOp('a')
    b = BosonOp('b')

    assert isinstance(a, BosonOp)
    assert isinstance(Dagger(a), BosonOp)

    assert a.is_annihilation
    assert not Dagger(a).is_annihilation

    assert BosonOp("a") == BosonOp("a", True)
    assert BosonOp("a") != BosonOp("c")
    assert BosonOp("a", True) != BosonOp("a", False)

    assert Commutator(a, Dagger(a)).doit() == 1

    assert Commutator(a, Dagger(b)).doit() == a * Dagger(b) - Dagger(b) * a

    assert Dagger(exp(a)) == exp(Dagger(a))

