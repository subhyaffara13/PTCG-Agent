
def test_Union_contains():
    assert zoo not in Union(
        Interval.open(-oo, 0), Interval.open(0, oo))

