
def test_union_intersection_constructor():
    # The actual exception does not matter here, so long as these fail
    sets = [FiniteSet(1), FiniteSet(2)]
    raises(Exception, lambda: Union(sets))
    raises(Exception, lambda: Intersection(sets))
    raises(Exception, lambda: Union(tuple(sets)))
    raises(Exception, lambda: Intersection(tuple(sets)))
    raises(Exception, lambda: Union(i for i in sets))
    raises(Exception, lambda: Intersection(i for i in sets))

    # Python sets are treated the same as FiniteSet
    # The union of a single set (of sets) is the set (of sets) itself
    assert Union(set(sets)) == FiniteSet(*sets)
    assert Intersection(set(sets)) == FiniteSet(*sets)

    assert Union({1}, {2}) == FiniteSet(1, 2)
    assert Intersection({1, 2}, {2, 3}) == FiniteSet(2)

