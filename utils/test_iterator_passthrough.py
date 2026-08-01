
def test_iterator_passthrough():
    """#181: iterator passthrough did not compile"""
    from pybind11_tests.sequences_and_iterators import iterator_passthrough

    values = [3, 5, 7, 9, 11, 13, 15]
    assert list(iterator_passthrough(iter(values))) == values

