
def test_Gens_preprocess():
    assert Gens.preprocess((None,)) == ()
    assert Gens.preprocess((x, y, z)) == (x, y, z)
    assert Gens.preprocess(((x, y, z),)) == (x, y, z)

    a = Symbol('a', commutative=False)

    raises(GeneratorsError, lambda: Gens.preprocess((x, x, y)))
    raises(GeneratorsError, lambda: Gens.preprocess((x, y, a)))

