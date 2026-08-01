
def test_Singletons():
    protocols = [0, 1, 2, 3, 4]
    copiers = [copy.copy, copy.deepcopy]
    copiers += [lambda x: pickle.loads(pickle.dumps(x, proto))
            for proto in protocols]
    if cloudpickle:
        copiers += [lambda x: cloudpickle.loads(cloudpickle.dumps(x))]

    for obj in (Integer(-1), Integer(0), Integer(1), Rational(1, 2), pi, E, I,
            oo, -oo, zoo, nan, S.GoldenRatio, S.TribonacciConstant,
            S.EulerGamma, S.Catalan, S.EmptySet, S.IdentityFunction):
        for func in copiers:
            assert func(obj) is obj


def test_Singletons():
    sT(S.Catalan, 'Catalan')
    sT(S.ComplexInfinity, 'zoo')
    sT(S.EulerGamma, 'EulerGamma')
    sT(S.Exp1, 'E')
    sT(S.GoldenRatio, 'GoldenRatio')
    sT(S.TribonacciConstant, 'TribonacciConstant')
    sT(S.Half, 'Rational(1, 2)')
    sT(S.ImaginaryUnit, 'I')
    sT(S.Infinity, 'oo')
    sT(S.NaN, 'nan')
    sT(S.NegativeInfinity, '-oo')
    sT(S.NegativeOne, 'Integer(-1)')
    sT(S.One, 'Integer(1)')
    sT(S.Pi, 'pi')
    sT(S.Zero, 'Integer(0)')
    sT(S.Complexes, 'Complexes')
    sT(S.EmptySequence, 'EmptySequence')
    sT(S.EmptySet, 'EmptySet')
    # sT(S.IdentityFunction, 'Lambda(_x, _x)')
    sT(S.Naturals, 'Naturals')
    sT(S.Naturals0, 'Naturals0')
    sT(S.Rationals, 'Rationals')
    sT(S.Reals, 'Reals')
    sT(S.UniversalSet, 'UniversalSet')

