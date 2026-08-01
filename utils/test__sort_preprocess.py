
def test_Sort_preprocess():
    assert Sort.preprocess([x, y, z]) == ['x', 'y', 'z']
    assert Sort.preprocess((x, y, z)) == ['x', 'y', 'z']

    assert Sort.preprocess('x > y > z') == ['x', 'y', 'z']
    assert Sort.preprocess('x>y>z') == ['x', 'y', 'z']

    raises(OptionError, lambda: Sort.preprocess(0))
    raises(OptionError, lambda: Sort.preprocess({x, y, z}))

