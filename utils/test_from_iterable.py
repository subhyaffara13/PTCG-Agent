
def test_from_iterable(pytype, from_iter_func):
    my_iter = iter(range(10))
    s = from_iter_func(my_iter)
    assert type(s) == pytype
    assert s == pytype(range(10))

