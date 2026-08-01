
def test_deprecated_iterables():
    from sympy.utilities.iterables import default_sort_key, ordered
    with warns_deprecated_sympy():
        assert list(ordered([y, x])) == [x, y]
    with warns_deprecated_sympy():
        assert sorted([y, x], key=default_sort_key) == [x, y]

