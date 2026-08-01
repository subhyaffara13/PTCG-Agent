
def test_iterator_rvp():
    """#388: Can't make iterators via make_iterator() with different r/v policies"""
    import pybind11_tests.sequences_and_iterators as m

    assert list(m.make_iterator_1()) == [1, 2, 3]
    assert list(m.make_iterator_2()) == [1, 2, 3]
    assert not isinstance(m.make_iterator_1(), type(m.make_iterator_2()))

