
def test_Domain_postprocess():
    raises(GeneratorsError, lambda: Domain.postprocess({'gens': (x, y),
           'domain': ZZ[y, z]}))

    raises(GeneratorsError, lambda: Domain.postprocess({'gens': (),
           'domain': EX}))
    raises(GeneratorsError, lambda: Domain.postprocess({'domain': EX}))

