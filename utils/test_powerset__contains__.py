
def test_powerset__contains__():
    subset_series = [
        S.EmptySet,
        FiniteSet(1, 2),
        S.Naturals,
        S.Naturals0,
        S.Integers,
        S.Rationals,
        S.Reals,
        S.Complexes]

    l = len(subset_series)
    for i in range(l):
        for j in range(l):
            if i <= j:
                assert subset_series[i] in \
                    PowerSet(subset_series[j], evaluate=False)
            else:
                assert subset_series[i] not in \
                    PowerSet(subset_series[j], evaluate=False)

