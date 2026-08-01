
def test_contains_rangeindex_categories_no_engine():
    ci = CategoricalIndex(range(3))
    assert 2 in ci
    assert 5 not in ci
    assert "_engine" not in ci._cache

